import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Department } from "../services/department.model";
import { Router } from '@angular/router';
import { Location } from "@angular/common";




@Component({
    selector: 'app-departments',
    templateUrl: './departments.component.html',
    styleUrls: ['./departments.component.css']
})
export class DepartmentsComponent implements OnInit, OnDestroy {
    title = 'Departments'

    departmentsListSubs: Subscription = new Subscription;
    allDepartments: Department[] = [];
    departmentList: Department[] = [];

    selectedDepartment: string = "all";

    constructor(public DB: DBApiService, private router: Router, private location: Location) {}

    ngOnInit(): void {
        this.departmentsListSubs = this.DB.getDepartments().subscribe(
            data => {
                this.allDepartments = data;
                this.departmentList = data;
            }
        );
        
    }

    viewDepartment(): void {
        if (this.selectedDepartment == "all") {
            this.departmentsListSubs = this.DB.getDepartments().subscribe(
                data => {
                    this.departmentList = data;
                }
            );
            return;
        }
        this.location.replaceState(`/department/${this.selectedDepartment}`)
        this.departmentsListSubs = this.DB.getSpecificDepartment(this.selectedDepartment).subscribe(
            data => {
                this.departmentList = [data];
            }
        );

    }

    newDepartment(){
        console.log("New Department");
        this.router.navigateByUrl('/add-department');
    }

    ngOnDestroy(): void {
        this.departmentsListSubs.unsubscribe();
        
    }
}