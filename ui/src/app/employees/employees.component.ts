import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Employee } from "../services/employee.model";
import { Router } from '@angular/router';




@Component({
    selector: 'app-employees',
    templateUrl: './employees.component.html',
    styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit, OnDestroy {
    title = 'Onboarded Employees'

    employeesListSubs: Subscription = new Subscription;
    allEmployees: Employee[] = [];
    employeesList: Employee[] = [];

    selectedDate: string = "all";

    constructor(public DB: DBApiService, private router: Router) {}

    ngOnInit(): void {
        this.employeesListSubs = this.DB.getEmployees().subscribe(
            data => {
                this.allEmployees = data;
                this.employeesList = data;
            }
        );
        
    }

    viewEmployee(): void {
        this.employeesListSubs = this.DB.getEmployees().subscribe(
            data => {
                this.employeesList = data;
            }
        );
    }

    newEmployee(){
        console.log("New Employee");
        this.router.navigateByUrl('/add-employee');
    }


    ngOnDestroy(): void {
        this.employeesListSubs.unsubscribe();
    }
}