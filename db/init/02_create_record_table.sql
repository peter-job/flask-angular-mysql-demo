-- Create the record table
CREATE TABLE record (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each water quality record',
    location VARCHAR(100) NOT NULL COMMENT 'Name of the location where the measurement was recorded',
    ph_level DECIMAL(4,2) NOT NULL COMMENT 'pH level of the water sample',
    turbidity DECIMAL(5,3) NOT NULL COMMENT 'Turbidity of the water sample in NTU',
    temperature DECIMAL(5,2) NOT NULL COMMENT 'Water temperature in Celsius',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created in the database',
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was updated in the database, if updated. Null if not updated',
    deleted_at TIMESTAMP COMMENT 'Timestamp when the record was deleted by the application, if deleted. Null if not deleted. Soft delete'
) COMMENT = 'Water quality measurements recorded at different locations';

-- Add indexes on record table
CREATE INDEX idx_location ON record (location);

-- Insert sample records
INSERT INTO record (location, ph_level, turbidity, temperature)
VALUES ('Murray River', 7.0, 1.21, 20.5),
       ('Lake Argyle', 7.5, 1.09, 21.0),
       ('Derwent River', 6.5, 1.50, 19.5);
