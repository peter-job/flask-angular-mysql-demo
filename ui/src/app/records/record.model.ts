/**
 * API Model for a water quality record
 */
export interface WaterQualityRecord {
  id?: number;
  location: string;
  ph_level: number;
  turbidity: number;
  temperature: number;
  created_at?: Date;
  updated_at?: Date | null;
  deleted_at?: Date | null;
}
