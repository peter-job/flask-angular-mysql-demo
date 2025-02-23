import { Component, OnInit, ViewChild } from "@angular/core";
import { RecordsService } from "./records.service";
import { WaterQualityRecord } from "./record.model";
import { CommonModule } from "@angular/common";
import { Table, TableModule } from "primeng/table";
import { InputTextModule } from "primeng/inputtext";
import { ButtonModule } from "primeng/button";
import { FormsModule } from "@angular/forms";
import { InputNumberModule } from "primeng/inputnumber";
import { TooltipModule } from "primeng/tooltip";
import { TooltipOptions } from "primeng/api";

@Component({
  selector: "app-records-table",
  templateUrl: "./records-table.component.html",
  standalone: true,
  imports: [
    CommonModule,
    TableModule,
    InputTextModule,
    ButtonModule,
    FormsModule,
    InputNumberModule,
    TooltipModule,
  ],
})
export class RecordsTableComponent implements OnInit {
  @ViewChild("editableTable") editableTable!: Table;

  records: WaterQualityRecord[] = [];

  tooltipOptions: TooltipOptions = {
    showDelay: 1000,
  };

  constructor(private recordsService: RecordsService) {}

  ngOnInit(): void {
    this.fetchRecords();
  }

  fetchRecords(): void {
    this.recordsService.getRecords().subscribe((data) => {
      console.debug("Records fetched", data);
      this.records = data;
    });
  }

  /**
   * Helper method to create a default record template.
   * When includeId is true, the record gets an id of 0 to indicate it's new.
   */
  private getNewRecordTemplate(): WaterQualityRecord {
    return {
      id: 0,
      location: "",
      ph_level: 7.0,
      turbidity: 0,
      temperature: 20,
    };
  }

  /**
   * Unified method to persist a record.
   * Creates the record if record.id === 0; otherwise, it updates.
   */
  private persistRecord(record: WaterQualityRecord): void {
    const action =
      record.id === 0
        ? this.recordsService.createRecord(record)
        : this.recordsService.updateRecord(record);
    action.subscribe((savedRecord) => {
      console.debug(
        record.id === 0 ? "Record created" : "Record saved",
        savedRecord,
      );
      this.fetchRecords();
    });
  }

  /**
   * Adds a new row to the table and starts inline editing.
   */
  addNewRow(): void {
    const newRecord = this.getNewRecordTemplate();
    this.records = [...this.records, newRecord];
    this.editableTable?.initRowEdit(newRecord);
  }

  onRowEditInit(record: WaterQualityRecord): void {
    console.debug("Editing started for:", record);
  }

  onRowEditSave(record: WaterQualityRecord): void {
    this.persistRecord(record);
  }

  onRowEditCancel(record: WaterQualityRecord, rowIndex: number): void {
    if (record.id === 0) {
      // Remove the unsaved new record if editing is canceled
      this.records.splice(rowIndex, 1);
    }
    console.debug("Editing cancelled for:", record);
  }

  deleteRecord(id: number): void {
    this.recordsService.deleteRecord(id).subscribe(() => {
      console.debug("Record deleted", id);
      this.fetchRecords();
    });
  }
}
