import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError, catchError } from "rxjs";


import { API_URL } from "../env";
import { AppError } from "../app-error";
import { Employee } from "./employee.model";
import { Department } from "./department.model";
import { Quota } from './quota.model';



@Injectable()
export class DBApiService {

    constructor(private http: HttpClient){
    }

    httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        })
    };

    getDepartments(): Observable<Department[]>{
        return this.http.get<Department[]>(`${API_URL}/departments`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getSpecificDepartment(department:string): Observable<Department>{
        return this.http.get<Department>(`${API_URL}/department/${department}`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );

    }

    addDepartment(department: Department): Observable<any>{
        return this.http.post<any>(`${API_URL}/add-department`, department, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getEmployees(): Observable<Employee[]>{
        return this.http.get<Employee[]>(`${API_URL}/employees`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getEmployeesDate(date: string): Observable<Employee[]>{
        return this.http.get<Employee[]>(`${API_URL}/employees/'${date}'`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    addEmployee(employee: Employee): Observable<any>{
        return this.http.post<any>(`${API_URL}/add-employee`, employee, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    editEmployee(login_id: string, body: Employee): Observable<any>{
        return this.http.put<any>(`${API_URL}/employee/${login_id}`, body, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }


    deleteEmployee(login_id: string): Observable<any>{
        return this.http.delete<any>(`${API_URL}/employee/${login_id}`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getEmployeeInfo(login_id: string): Observable<Employee>{
        return this.http.get<Employee>(`${API_URL}/employee/${login_id}`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }

    getEmployeeQuota(login_id: string): Observable<Quota>{
        return this.http.get<Quota>(`${API_URL}/quota/${login_id}`, this.httpOptions).pipe(
            catchError( (error: HttpErrorResponse) => {
                return throwError( () => new AppError(error))
            })
        );
    }
}