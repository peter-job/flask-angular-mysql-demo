import {
  ApplicationConfig,
  InjectionToken,
  provideZoneChangeDetection,
} from "@angular/core";
import { provideAnimationsAsync } from "@angular/platform-browser/animations/async";
import { provideRouter } from "@angular/router";
import Aura from "@primeng/themes/aura";
import { providePrimeNG } from "primeng/config";

import {
  HTTP_INTERCEPTORS,
  provideHttpClient,
  withInterceptorsFromDi,
} from "@angular/common/http";
import { routes } from "./app.routes";
import { HttpErrorInterceptor } from "./http-error.interceptor";
import { MessageService } from "primeng/api";

export const API_BASE_URL_INJECTION_TOKEN = new InjectionToken<string>(
  "API_BASE_URL",
);

// Hardcoded for demo
const API_BASE_URL = "http://127.0.0.1:5000";

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
        preset: Aura,
      },
    }),
    MessageService,
    provideHttpClient(withInterceptorsFromDi()),
    { provide: API_BASE_URL_INJECTION_TOKEN, useValue: API_BASE_URL },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpErrorInterceptor,
      multi: true,
    },
  ],
};
