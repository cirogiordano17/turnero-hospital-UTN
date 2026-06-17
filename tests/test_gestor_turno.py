"""
Tests unitarios para GestorTurno.

Demuestran la separación ECB: el Control se puede testear completamente
sin base de datos, reemplazando los DAOs con mocks (Dependency Inversion).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock, patch
from datetime import date, time

from control.gestor_turno import GestorTurno
from boundary.persistence.turno_dao import TurnoDAO
from boundary.persistence.medico_dao import MedicoDAO
from boundary.persistence.paciente_dao import PacienteDAO
from entities.exceptions import EntidadNoEncontradaError, EstadoInvalidoError


def _make_turno(estado="Libre") -> dict:
    return {
        "id_turno": 1, "estado": estado, "matricula": 123,
        "id_paciente": None, "fecha": date(2026, 7, 1),
        "hora_inicio": time(9, 0), "hora_fin": time(9, 30),
    }


def _make_paciente() -> dict:
    return {"id_paciente": 42, "nombre": "Carlos", "apellido": "López", "activo": 1}


class TestGestorTurnoProgramar(unittest.TestCase):
    """
    Caso de uso: Programar turno
    """

    def setUp(self):
        self.turno_dao = MagicMock(spec=TurnoDAO)
        self.medico_dao = MagicMock(spec=MedicoDAO)
        self.paciente_dao = MagicMock(spec=PacienteDAO)
        self.gestor = GestorTurno(self.turno_dao, self.medico_dao, self.paciente_dao)

    def test_programar_turno_exitoso(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Libre")
        self.paciente_dao.buscar_por_id.return_value = _make_paciente()
        self.turno_dao.programar.return_value = True
        self.turno_dao.buscar_por_id.side_effect = [
            _make_turno("Libre"),
            {**_make_turno("Programado"), "id_paciente": 42},
        ]

        resultado = self.gestor.programar_turno(1, 42)

        self.turno_dao.programar.assert_called_once_with(1, 42, None, "")
        self.assertEqual(resultado["estado"], "Programado")

    def test_programar_turno_no_encontrado_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = None

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.programar_turno(99, 42)

    def test_programar_turno_no_libre_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Programado")

        with self.assertRaises(EstadoInvalidoError):
            self.gestor.programar_turno(1, 42)

    def test_programar_paciente_no_existe_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Libre")
        self.paciente_dao.buscar_por_id.return_value = None

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.programar_turno(1, 999)

    def test_programar_con_especialidad(self):
        self.turno_dao.buscar_por_id.side_effect = [
            _make_turno("Libre"),
            {**_make_turno("Programado"), "id_paciente": 42, "id_especialidad": 5},
        ]
        self.paciente_dao.buscar_por_id.return_value = _make_paciente()
        self.turno_dao.programar.return_value = True

        self.gestor.programar_turno(1, 42, id_especialidad=5)

        self.turno_dao.programar.assert_called_once_with(1, 42, 5, "")


class TestGestorTurnoCancelar(unittest.TestCase):

    def setUp(self):
        self.turno_dao = MagicMock(spec=TurnoDAO)
        self.gestor = GestorTurno(self.turno_dao,
                                   MagicMock(spec=MedicoDAO),
                                   MagicMock(spec=PacienteDAO))

    def test_cancelar_turno_programado_exitoso(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Programado")
        self.turno_dao.cambiar_estado.return_value = True

        resultado = self.gestor.cancelar_turno(1)

        self.assertTrue(resultado)
        self.turno_dao.cambiar_estado.assert_called_once_with(1, "Cancelado")

    def test_cancelar_turno_no_encontrado_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = None

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.cancelar_turno(99)

    def test_cancelar_turno_libre_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Libre")

        with self.assertRaises(EstadoInvalidoError):
            self.gestor.cancelar_turno(1)

    def test_cancelar_turno_atendido_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Atendido")

        with self.assertRaises(EstadoInvalidoError):
            self.gestor.cancelar_turno(1)


class TestGestorTurnoInasistencia(unittest.TestCase):

    def setUp(self):
        self.turno_dao = MagicMock(spec=TurnoDAO)
        self.gestor = GestorTurno(self.turno_dao,
                                   MagicMock(spec=MedicoDAO),
                                   MagicMock(spec=PacienteDAO))

    def test_marcar_inasistencia_exitoso(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Programado")
        self.turno_dao.cambiar_estado.return_value = True

        resultado = self.gestor.registrar_inasistencia(1)

        self.assertTrue(resultado)
        self.turno_dao.cambiar_estado.assert_called_once_with(1, "Inasistencia")

    def test_marcar_inasistencia_turno_atendido_lanza_excepcion(self):
        self.turno_dao.buscar_por_id.return_value = _make_turno("Atendido")

        with self.assertRaises(EstadoInvalidoError):
            self.gestor.registrar_inasistencia(1)


class TestGestorTurnoInasistenciaAutomatica(unittest.TestCase):

    def setUp(self):
        self.turno_dao = MagicMock(spec=TurnoDAO)
        self.gestor = GestorTurno(self.turno_dao,
                                   MagicMock(spec=MedicoDAO),
                                   MagicMock(spec=PacienteDAO))

    def test_marcar_inasistencias_automaticas_llama_dao(self):
        self.turno_dao.marcar_inasistencias_vencidas.return_value = 3

        cantidad = self.gestor.marcar_inasistencias_automaticas()

        self.assertEqual(cantidad, 3)
        self.turno_dao.marcar_inasistencias_vencidas.assert_called_once()


if __name__ == "__main__":
    unittest.main()
