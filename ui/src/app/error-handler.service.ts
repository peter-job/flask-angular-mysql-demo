import { HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { MessageService } from "primeng/api";

@Injectable({
  providedIn: "root",
})
export class ErrorHandlerService {
  constructor(private messageService: MessageService) {}

  handleHttpError(error: HttpErrorResponse): void {
    console.debug("Intercepted error", error);
    const summary = error.statusText;
    const detail = error.error.message || error.message;
    this.messageService.add({ severity: "error", summary, detail });
  }
}
