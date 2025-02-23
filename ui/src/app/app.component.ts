import { Component } from "@angular/core";
import { RecordsTableComponent } from "./records/records-table.component";
import { ToastModule } from "primeng/toast";

/**
 * Root component for the application
 */
@Component({
  selector: "app-root",
  imports: [RecordsTableComponent, ToastModule],
  templateUrl: "./app.component.html",
})
export class AppComponent {
  title = "app";
}
