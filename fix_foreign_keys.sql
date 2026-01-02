-- Active: 1766547367368@@127.0.0.1@3306@copymart
-- Desactivar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS=0;

-- Eliminar las restricciones existentes
ALTER TABLE clients DROP FOREIGN KEY clients_ibfk_1;
ALTER TABLE contacts DROP FOREIGN KEY contacts_ibfk_1;
ALTER TABLE sales DROP FOREIGN KEY sales_ibfk_1;
ALTER TABLE branches DROP FOREIGN KEY branches_ibfk_1;
ALTER TABLE areas DROP FOREIGN KEY areas_ibfk_1;
ALTER TABLE rents DROP FOREIGN KEY rents_ibfk_1;
ALTER TABLE billings DROP FOREIGN KEY billings_ibfk_1;

-- Recrear las restricciones con ON DELETE CASCADE
-- clients.contact_id -> contacts.contact_id
ALTER TABLE clients 
ADD CONSTRAINT clients_ibfk_1 
FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE SET NULL;

-- contacts.client_id -> clients.client_id
ALTER TABLE contacts 
ADD CONSTRAINT contacts_ibfk_1 
FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE;

-- sales.client_id -> clients.client_id
ALTER TABLE sales 
ADD CONSTRAINT sales_ibfk_1 
FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE;

-- branches.client_id -> clients.client_id
ALTER TABLE branches 
ADD CONSTRAINT branches_ibfk_1 
FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE;

-- areas.branch_id -> branches.branch_id
ALTER TABLE areas 
ADD CONSTRAINT areas_ibfk_1 
FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE CASCADE;

-- rents.client_id -> clients.client_id
ALTER TABLE rents 
ADD CONSTRAINT rents_ibfk_1 
FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE;

-- billings.client_id -> clients.client_id
ALTER TABLE billings 
ADD CONSTRAINT billings_ibfk_1 
FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS=1;
