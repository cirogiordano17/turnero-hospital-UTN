"""Tests unitarios para GestorPaciente."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock
from datetime import date

from control.gestor_paciente import GestorPaciente
from boundary.persistence.paciente_dao import PacienteDAO
from entities.paciente import Paciente
from entities.exceptions import EntidadNoEncontradaError, DuplicadoError, ValidacionError


def _row_paciente(**kwargs):
    defaults = dict(id_paciente=1, nombre="Carlos", apellido="López",
                    telefono="1145678901", fecha_nacimiento=date(1990, 5, 15),
                    direccion="Av. Corrientes 1234", activo=1)
    defaults.update(kwargs)
    return defaults


class TestGestorPacienteRegistrar(unittest.TestCase):

    def setUp(self):
        self.dao = MagicMock(spec=PacienteDAO)
        self.gestor = GestorPaciente(self.dao)

    def test_registrar_paciente_nuevo(self):
        self.dao.buscar_por_id.return_value = None
        self.dao.insertar.return_value = True

        paciente = self.gestor.registrar_paciente(
            1, "Carlos", "López", "1145678901",
            date(1990, 5, 15), "Av. Corrientes 1234",
        )

        self.assertIsInstance(paciente, Paciente)
        self.dao.insertar.assert_called_once()

    def test_registrar_paciente_duplicado_lanza_excepcion(self):
        self.dao.buscar_por_id.return_value = _row_paciente()

        with self.assertRaises(DuplicadoError):
            self.gestor.registrar_paciente(
                1, "Carlos", "López", "1145678901",
                date(1990, 5, 15), "Av. Corrientes 1234",
            )

    def test_registrar_nombre_vacio_lanza_excepcion(self):
        self.dao.buscar_por_id.return_value = None

        with self.assertRaises(ValidacionError):
            self.gestor.registrar_paciente(
                99, "", "López", "1145678901",
                date(1990, 5, 15), "Av. Corrientes 1234",
            )


class TestGestorPacienteBaja(unittest.TestCase):

    def setUp(self):
        self.dao = MagicMock(spec=PacienteDAO)
        self.gestor = GestorPaciente(self.dao)

    def test_dar_de_baja_existente(self):
        self.dao.buscar_por_id.return_value = _row_paciente()

        self.gestor.dar_de_baja(1)

        self.dao.dar_de_baja.assert_called_once_with(1)

    def test_dar_de_baja_no_existente_lanza_excepcion(self):
        self.dao.buscar_por_id.return_value = None

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.dar_de_baja(999)


class TestGestorPacienteHistorial(unittest.TestCase):

    def setUp(self):
        self.dao = MagicMock(spec=PacienteDAO)
        self.gestor = GestorPaciente(self.dao)

    def test_obtener_historial_paciente_existente(self):
        self.dao.buscar_por_id.return_value = _row_paciente()
        self.dao.obtener_historial.return_value = [{"id_historial": 1}]

        resultado = self.gestor.obtener_historial(1)

        self.assertEqual(len(resultado), 1)

    def test_obtener_historial_paciente_no_existe_lanza_excepcion(self):
        self.dao.buscar_por_id.return_value = None

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.obtener_historial(999)


if __name__ == "__main__":
    unittest.main()
