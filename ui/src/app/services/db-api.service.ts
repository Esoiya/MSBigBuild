import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, catchError } from "rxjs";


import { API_URL } from "../env";
import { AppError } from "../app-error";
import { Employee } from "./employee.model";
import { Department } from "./department.model";



@Injectable()
export class DBApiService {

    constructor(private http: HttpClient){

    }

    getDepartments(): Observable<Department[]>{
        return this.http.get<Department[]>(`${API_URL}/departments`).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getSpecificDepartment(department:string): Observable<Department>{
        return this.http.get<Department>(`${API_URL}/department/${department}`).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );

    }

    addDepartment(department: Department): Observable<any>{
        return this.http.post<any>(`${API_URL}/add-department`, department).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getEmployees(): Observable<Employee[]>{
        return this.http.get<Employee[]>(`${API_URL}/employees`).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    addEmployee(employee: Employee): Observable<any>{
        return this.http.post<any>(`${API_URL}/add-employee`, employee).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }



}