-- Ubicación en contactos
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS latitude FLOAT NULL;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS longitude FLOAT NULL;

-- Ubicación en sucursales
ALTER TABLE branches ADD COLUMN IF NOT EXISTS latitude FLOAT NULL;
ALTER TABLE branches ADD COLUMN IF NOT EXISTS longitude FLOAT NULL;
