import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Employee } from "../services/employee.model";
import { Router } from '@angular/router';
import { Location } from "@angular/common";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { Department } from "../services/department.model";




@Component({
    selector: 'app-add-department',
    templateUrl: './add-department.component.html',
    styleUrls: ['./add-department.component.css']
})
export class AddDepartmentComponent implements OnInit, OnDestroy {
    title = 'Add New Department'

    newDepartmentSubs: Subscription = new Subscription;

    newDepartment!: Department;

    departmentIDList: Department[] = [];

    departmentForm! : FormGroup;

    constructor(public DB: DBApiService, private router: Router, private location: Location) {}

    ngOnInit(): void {
        this.newDepartmentSubs = this.DB.getDepartments().subscribe(
            data => {
                this.departmentIDList = data;
                // TODO - get only department IDs
            }
        );

        this.departmentForm = new FormGroup({
            dept_id: new FormControl(
                '',
                [
                    Validators.required
                    // TODO add check dept_id exists in departmentID list
                ]
            ),
            code: new FormControl(
                '',
                [
                    Validators.required
                ]
            ),
            description: new FormControl(
                '',
                [Validators.required]
            )
            
        })
        
    }

    get dept_id() {
        return this.departmentForm.get('dept_id')!;
    }

    get name() {
        return this.departmentForm.get('code')!;
    }

    get onboarded(){
        return this.departmentForm.get('description')!;
    }

    addDepartment(): void {
        this.newDepartment = new Department(
            this.departmentForm.value.dept_id,
            this.departmentForm.value.code,
            this.departmentForm.value.description
        );
        console.log(this.newDepartment);
        this.newDepartmentSubs = this.DB.addDepartment(this.newDepartment).subscribe(
            status => console.log(status)
        );
    }


    viewAllDepartments(): void {
        console.log("Back to Onboarded Employees");
        this.router.navigateByUrl('/employees');
    }

    ngOnDestroy(): void {
        this.newDepartmentSubs.unsubscribe();
        
    }
}