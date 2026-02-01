-- Active: 1766547367368@@127.0.0.1@3306@copymart
-- Script para agregar las columnas start_date y end_date a la tabla rents

-- Verificar si las columnas ya existen
-- Si no existen, agregarlas

-- Agregar start_date si no existe
ALTER TABLE rents 
ADD COLUMN IF NOT EXISTS start_date DATE NOT NULL DEFAULT '2024-01-01' AFTER contract_status;

-- Agregar end_date si no existe  
ALTER TABLE rents
ADD COLUMN IF NOT EXISTS end_date DATE NULL AFTER start_date;

-- Opcional: Eliminar el default de start_date después de agregar valores reales
-- ALTER TABLE rents ALTER COLUMN start_date DROP DEFAULT;
