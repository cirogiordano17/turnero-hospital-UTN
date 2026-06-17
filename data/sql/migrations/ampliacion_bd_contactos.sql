USE hospital_db;

CREATE TABLE IF NOT EXISTS Contactos_Paciente (
    id_contacto INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    tipo_contacto VARCHAR(20) NOT NULL,
    valor_contacto VARCHAR(100) NOT NULL,
    es_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE
) ENGINE=InnoDB;
