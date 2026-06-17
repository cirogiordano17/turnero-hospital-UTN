"""
Tests unitarios para la capa Entity.

Verifican que las entidades cumplan sus invariantes de dominio
sin necesidad de base de datos ni servicios externos.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import date, time

from entities.medico import Medico
from entities.paciente import Paciente
from entities.turno import Turno
from entities.agenda import Agenda
from entities.especialidad import Especialidad
from entities.exceptions import ValidacionError, EstadoInvalidoError
from entities.states.libre import Libre
from entities.states.programado import Programado
from entities.states.atendido import Atendido
from entities.states.cancelado import Cancelado
from entities.states.inasistencia import Inasistencia


class TestMedico(unittest.TestCase):

    def _medico(self, **kwargs):
        defaults = dict(
            matricula=1234,
            nombre="Ana",
            apellido="García",
            telefono="1134567890",
            email="ana.garcia@hospital.com",
            fecha_alta=date(2020, 1, 1),
        )
        defaults.update(kwargs)
        return Medico(**defaults)

    def test_creacion_correcta(self):
        m = self._medico()
        self.assertEqual(m.matricula, 1234)
        self.assertEqual(m.nombre_completo, "Ana García")

    def test_email_invalido_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            self._medico(email="no-es-un-email")

    def test_nombre_vacio_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            self._medico(nombre="")

    def test_esta_activo_sin_fecha_baja(self):
        m = self._medico()
        self.assertTrue(m.esta_activo)

    def test_esta_inactivo_con_fecha_baja(self):
        m = self._medico()
        m.fecha_baja = date(2024, 6, 1)
        self.assertFalse(m.esta_activo)

    def test_fecha_baja_anterior_alta_lanza_excepcion(self):
        m = self._medico(fecha_alta=date(2023, 1, 1))
        with self.assertRaises(ValidacionError):
            m.fecha_baja = date(2022, 1, 1)

    def test_email_se_normaliza_a_minusculas(self):
        m = self._medico(email="ANA@Hospital.COM")
        self.assertEqual(m.email, "ana@hospital.com")

    def test_igualdad_por_matricula(self):
        m1 = self._medico(matricula=100)
        m2 = self._medico(matricula=100, nombre="Otro")
        self.assertEqual(m1, m2)

    def test_desigualdad_distinta_matricula(self):
        m1 = self._medico(matricula=100)
        m2 = self._medico(matricula=200)
        self.assertNotEqual(m1, m2)


class TestPaciente(unittest.TestCase):

    def _paciente(self, **kwargs):
        defaults = dict(
            id_paciente=1,
            nombre="Carlos",
            apellido="López",
            telefono="1145678901",
            fecha_nacimiento=date(1990, 5, 15),
            direccion="Av. Corrientes 1234",
        )
        defaults.update(kwargs)
        return Paciente(**defaults)

    def test_creacion_correcta(self):
        p = self._paciente()
        self.assertEqual(p.nombre_completo, "Carlos López")

    def test_nombre_vacio_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            self._paciente(nombre="  ")

    def test_telefono_puede_estar_vacio(self):
        p = self._paciente(telefono="")
        self.assertEqual(p.telefono, "")


class TestTurno(unittest.TestCase):

    def _turno(self, estado="Libre"):
        return Turno(
            id_turno=1,
            matricula_medico=123,
            id_consultorio=2,
            id_agenda=5,
            fecha=date(2026, 7, 1),
            hora_inicio=time(9, 0),
            hora_fin=time(9, 30),
            estado=estado,
        )

    def test_estado_inicial_libre(self):
        t = self._turno()
        self.assertIsInstance(t.estado, Libre)

    def test_programar_turno_libre(self):
        t = self._turno()
        t.programar(id_paciente=42)
        self.assertIsInstance(t.estado, Programado)
        self.assertEqual(t.id_paciente, 42)

    def test_programar_registra_cambio_de_estado(self):
        t = self._turno()
        t.programar(id_paciente=42)
        self.assertEqual(len(t.cambios), 1)
        self.assertEqual(t.cambios[0].estado.nombre, "Programado")

    def test_cancelar_turno_programado(self):
        t = self._turno(estado="Programado")
        t.cancelar()
        self.assertIsInstance(t.estado, Cancelado)

    def test_cancelar_turno_libre_lanza_excepcion(self):
        t = self._turno()
        with self.assertRaises(EstadoInvalidoError):
            t.cancelar()

    def test_atender_turno_programado(self):
        t = self._turno(estado="Programado")
        t.atender()
        self.assertIsInstance(t.estado, Atendido)

    def test_atender_turno_libre_lanza_excepcion(self):
        t = self._turno()
        with self.assertRaises(EstadoInvalidoError):
            t.atender()

    def test_marcar_inasistencia_programado(self):
        t = self._turno(estado="Programado")
        t.marcar_inasistencia()
        self.assertIsInstance(t.estado, Inasistencia)

    def test_hora_fin_anterior_inicio_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            Turno(
                id_turno=1, matricula_medico=1, id_consultorio=1, id_agenda=1,
                fecha=date(2026, 7, 1),
                hora_inicio=time(10, 0),
                hora_fin=time(9, 0),
            )

    def test_estado_desconocido_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            self._turno(estado="EstadoInventado")

    def test_constructor_no_modifica_entidades_externas(self):
        """El constructor de Turno no debe tener side effects sobre Medico ni Paciente."""
        # Si el test puede crear un Turno sin pasar objetos Medico/Paciente completos,
        # confirma que no hay acoplamiento en el constructor.
        t = self._turno()
        self.assertIsNone(t.id_paciente)


class TestAgenda(unittest.TestCase):

    def test_capacidad_calcula_correctamente(self):
        """09:00 - 17:00 = 8h = 480min / 30 = 16 turnos"""
        agenda = Agenda(1, 123, 2, "Lunes", time(9, 0), time(17, 0))
        self.assertEqual(agenda.capacidad_turnos, 16)

    def test_dia_invalido_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            Agenda(1, 123, 2, "Holíday", time(9, 0), time(17, 0))

    def test_hora_fin_anterior_inicio_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            Agenda(1, 123, 2, "Lunes", time(17, 0), time(9, 0))


class TestEspecialidad(unittest.TestCase):

    def test_nombre_vacio_lanza_excepcion(self):
        with self.assertRaises(ValidacionError):
            Especialidad(1, "", "desc")

    def test_nombre_se_normaliza(self):
        e = Especialidad(1, "  Cardiología  ", "")
        self.assertEqual(e.nombre, "Cardiología")

    def test_igualdad_por_id(self):
        e1 = Especialidad(1, "Cardiología", "")
        e2 = Especialidad(1, "Otro nombre", "")
        self.assertEqual(e1, e2)


if __name__ == "__main__":
    unittest.main()
