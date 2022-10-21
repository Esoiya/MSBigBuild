import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Employee } from "../services/employee.model";
// import { Router } from '@angular/router';
import { ActivatedRoute } from "@angular/router";




@Component({
    selector: 'app-view-employee',
    templateUrl: './view-employee.component.html',
    styleUrls: ['./view-employee.component.css']
})
export class ViewEmployeeComponent implements OnInit, OnDestroy {
    title = 'Storage Utilisation'
    employee = ''

    employeesListSubs: Subscription = new Subscription;
    allEmployees: Employee[] = [];
    employeesList: Employee[] = [];

    selectedDate: string = "all";

    constructor(public DB: DBApiService, private route: ActivatedRoute) {}

    ngOnInit(): void {
        this.route.queryParams
            .subscribe(params => {
                console.log("params: " + params["employee"]);
                this.employee = params["employee"];
            });
        
        // this.employeesListSubs = this.DB.getEmployees().subscribe(
        //     data => {
        //         this.allEmployees = data;
        //         this.employeesList = data;
        //     }
        // );

        this.employeesListSubs = this.DB.getOneEmployee(this.employee).subscribe(
            data => {
                this.allEmployees = data;
                this.employeesList = data;
            }
        );
    }

    ngOnDestroy(): void {
        this.employeesListSubs.unsubscribe();
    }
}
