import { Injectable, Inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { WaterQualityRecord } from "./record.model";
import { API_BASE_URL_INJECTION_TOKEN } from "../app.config";
import { Observable } from "rxjs";

/**
 * Service for managing water quality records
 */
@Injectable({
  providedIn: "root",
})
export class RecordsService {
  private recordsUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(API_BASE_URL_INJECTION_TOKEN) private apiBaseUrl: string,
  ) {
    this.recordsUrl = `${this.apiBaseUrl}/water-quality/records`;
  }

  /**
   * GET all records (that haven’t been soft-deleted)
   */
  getRecords(): Observable<WaterQualityRecord[]> {
    return this.http.get<WaterQualityRecord[]>(this.recordsUrl);
  }

  /**
   * POST a new record
   */
  createRecord(
    record: Partial<WaterQualityRecord>,
  ): Observable<WaterQualityRecord> {
    return this.http.post<WaterQualityRecord>(this.recordsUrl, record);
  }

  /**
   * PATCH (update) an existing record
   */
  updateRecord(record: WaterQualityRecord): Observable<WaterQualityRecord> {
    const url = `${this.recordsUrl}/${record.id}`;
    return this.http.patch<WaterQualityRecord>(url, record);
  }

  /**
   * DELETE (soft-delete) a record
   */
  deleteRecord(id: number): Observable<object> {
    const url = `${this.recordsUrl}/${id}`;
    return this.http.delete(url);
  }
}
