PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categorias (
 id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
 nombre TEXT NOT NULL UNIQUE,
 descripcion TEXT
);
CREATE TABLE IF NOT EXISTS smartwatches (
 id_smartwatch INTEGER PRIMARY KEY AUTOINCREMENT,
 id_categoria INTEGER NOT NULL,
 nombre TEXT NOT NULL,
 modelo TEXT NOT NULL,
 precio INTEGER NOT NULL CHECK(precio >= 0),
 tamano_mm INTEGER CHECK(tamano_mm IS NULL OR tamano_mm > 0),
 tipo_pantalla TEXT,
 compatibilidad TEXT,
 descripcion TEXT,
 FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS caracteristicas (
 id_caracteristica INTEGER PRIMARY KEY AUTOINCREMENT,
 nombre TEXT NOT NULL UNIQUE,
 descripcion TEXT
);
CREATE TABLE IF NOT EXISTS smartwatch_caracteristicas (
 id_smartwatch INTEGER NOT NULL,
 id_caracteristica INTEGER NOT NULL,
 PRIMARY KEY (id_smartwatch,id_caracteristica),
 FOREIGN KEY (id_smartwatch) REFERENCES smartwatches(id_smartwatch) ON DELETE CASCADE,
 FOREIGN KEY (id_caracteristica) REFERENCES caracteristicas(id_caracteristica) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_smartwatches_categoria ON smartwatches(id_categoria);
CREATE INDEX IF NOT EXISTS idx_smartwatches_precio ON smartwatches(precio);
CREATE INDEX IF NOT EXISTS idx_sc_caracteristica ON smartwatch_caracteristicas(id_caracteristica);
