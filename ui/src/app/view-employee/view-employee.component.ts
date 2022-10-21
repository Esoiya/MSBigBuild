import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Employee } from "../services/employee.model";
// import { Router } from '@angular/router';
import { ActivatedRoute } from "@angular/router";
import { Quota } from "../services/quota.model";




@Component({
    selector: 'app-view-employee',
    templateUrl: './view-employee.component.html',
    styleUrls: ['./view-employee.component.css']
})
export class ViewEmployeeComponent implements OnInit, OnDestroy {
    title = 'Storage Utilisation';
    loginID: string = '';

    employeeListSubs: Subscription = new Subscription;
    employeeInfo: Employee[] = [];
    employeeQuota: Quota[] = [];

    selectedDate: string = "all";

    constructor(public DB: DBApiService, private route: ActivatedRoute) {}

    ngOnInit(): void {
        this.route.queryParams
            .subscribe(params => {
                this.loginID = params["employee"];
            });

        console.log(this.loginID);

        this.employeeListSubs = this.DB.getEmployeeInfo(this.loginID).subscribe(
            data => {
                this.employeeInfo = [data];
            }
        )

        this.employeeListSubs = this.DB.getEmployeeQuota(this.loginID).subscribe(
            data => {
                this.employeeQuota = [data];
            }
        )

        console.log(this.employeeQuota);

    }

    ngOnDestroy(): void {
        this.employeeListSubs.unsubscribe();
    }
}
