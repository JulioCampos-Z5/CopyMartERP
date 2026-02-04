-- Hacer que sparepart_id sea nullable en la tabla purchases
ALTER TABLE purchases MODIFY COLUMN sparepart_id INT NULL;
