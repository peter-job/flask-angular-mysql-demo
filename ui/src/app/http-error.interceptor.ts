import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, catchError, throwError } from "rxjs";
import { ErrorHandlerService } from "./error-handler.service";

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {
  constructor(private errorHandlingService: ErrorHandlerService) {}

  intercept(
    req: HttpRequest<unknown>,
    next: HttpHandler,
  ): Observable<HttpEvent<unknown>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        this.errorHandlingService.handleHttpError(error);
        return throwError(() => error);
      }),
    );
  }
}
