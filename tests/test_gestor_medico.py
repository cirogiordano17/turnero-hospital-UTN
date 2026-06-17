"""Tests unitarios para GestorMedico."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock
from datetime import date

from control.gestor_medico import GestorMedico
from boundary.persistence.medico_dao import MedicoDAO
from boundary.persistence.especialidad_dao import EspecialidadDAO
from entities.medico import Medico
from entities.exceptions import (
    EntidadNoEncontradaError, DuplicadoError, ValidacionError,
)


def _row_medico(**kwargs):
    defaults = dict(matricula=1234, nombre="Ana", apellido="García",
                    telefono="1134567890", email="ana@hospital.com",
                    fecha_ingreso=date(2020, 1, 1), activo=1)
    defaults.update(kwargs)
    return defaults


class TestGestorMedicoRegistrar(unittest.TestCase):

    def setUp(self):
        self.medico_dao = MagicMock(spec=MedicoDAO)
        self.esp_dao = MagicMock(spec=EspecialidadDAO)
        self.gestor = GestorMedico(self.medico_dao, self.esp_dao)

    def test_registrar_medico_nuevo(self):
        self.medico_dao.buscar_por_matricula.return_value = None
        self.medico_dao.insertar.return_value = True

        medico = self.gestor.registrar_medico(
            1234, "Ana", "García", "1134567890",
            "ana@hospital.com", date(2020, 1, 1),
        )

        self.assertIsInstance(medico, Medico)
        self.assertEqual(medico.matricula, 1234)
        self.medico_dao.insertar.assert_called_once()

    def test_registrar_medico_duplicado_lanza_excepcion(self):
        self.medico_dao.buscar_por_matricula.return_value = _row_medico()

        with self.assertRaises(DuplicadoError):
            self.gestor.registrar_medico(
                1234, "Ana", "García", "1134567890",
                "ana@hospital.com", date(2020, 1, 1),
            )

    def test_registrar_medico_email_invalido_lanza_excepcion(self):
        self.medico_dao.buscar_por_matricula.return_value = None

        with self.assertRaises(ValidacionError):
            self.gestor.registrar_medico(
                9999, "Test", "Test", "123",
                "email_invalido", date(2020, 1, 1),
            )

    def test_registrar_medico_con_especialidades(self):
        self.medico_dao.buscar_por_matricula.return_value = None
        self.medico_dao.insertar.return_value = True

        self.gestor.registrar_medico(
            1234, "Ana", "García", "1134567890",
            "ana@hospital.com", date(2020, 1, 1),
            especialidades_ids=[1, 2],
        )

        self.assertEqual(self.medico_dao.asignar_especialidad.call_count, 2)


class TestGestorMedicoBaja(unittest.TestCase):

    def setUp(self):
        self.medico_dao = MagicMock(spec=MedicoDAO)
        self.gestor = GestorMedico(self.medico_dao, MagicMock(spec=EspecialidadDAO))

    def test_dar_de_baja_existente(self):
        self.medico_dao.buscar_por_matricula.return_value = _row_medico()

        self.gestor.dar_de_baja(1234)

        self.medico_dao.dar_de_baja.assert_called_once_with(1234)

    def test_dar_de_baja_no_existente_lanza_excepcion(self):
        self.medico_dao.buscar_por_matricula.return_value = None

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.dar_de_baja(9999)


if __name__ == "__main__":
    unittest.main()
