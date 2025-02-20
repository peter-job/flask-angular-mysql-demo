-- Create the record table
CREATE TABLE record (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each water quality record',
    location VARCHAR(100) NOT NULL COMMENT 'Name of the location where the measurement was recorded',
    ph_level DECIMAL(4,2) NOT NULL COMMENT 'pH level of the water sample',
    turbidity DECIMAL(5,3) NOT NULL COMMENT 'Turbidity of the water sample in NTU',
    temperature DECIMAL(5,2) NOT NULL COMMENT 'Water temperature in Celsius',
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the measurement was recorded',
    -- Ensure uniqueness of (location, recorded_at)
    UNIQUE (location, recorded_at)
) COMMENT = 'Water quality measurements recorded at different locations';

-- Add indexes on record table
CREATE INDEX idx_location ON record (location);
CREATE INDEX idx_recorded_at ON record (recorded_at);

-- Insert sample record
INSERT INTO record (location, ph_level, turbidity, temperature, recorded_at)
VALUES ('Murray River', 7.0, 1.21, 20.5, '2025-01-01 12:00:00'),
       ('Lake Argyle', 7.5, 1.09, 21.0, '2025-01-01 12:00:00'),
       ('Derwent River', 6.5, 1.50, 19.5, '2025-01-01 12:00:00'),
       ('Murray River', 7.2, 1.29, 20.7, '2025-01-02 00:00:00'),
       ('Lake Argyle', 7.6, 1.11, 21.2, '2025-01-02 00:00:00'),
       ('Derwent River', 6.3, 1.55, 19.3, '2025-01-02 00:00:00');
