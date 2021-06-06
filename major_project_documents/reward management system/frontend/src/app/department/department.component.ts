import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { FormControl, FormGroup, FormBuilder, Validators, NgForm } from '@angular/forms';

@Component({
    selector: 'app-college',
    templateUrl: './department.component.html',
    styleUrls: ['./department.component.css']
})
export class DepartmentComponent {

    studentData;
    checkedBoxes;
    approved = false;
    loggedIn;
    invalid;
    login;

    collegeForm = new FormGroup({
    });

    form = new FormGroup({
        login: new FormControl(),
        password: new FormControl()
    });

    constructor(private fb: FormBuilder, private httpClient: HttpClient) {
        this.createForm();
    }
    createForm() {
        this.form = this.fb.group({
            login: ['', Validators.required],
            password: ['', Validators.required],
        });
    }


    ngOnInit() {
        this.loggedIn = false;
        this.invalid = false;
    }

    checkboxClicked(data) {
        console.log(data);
        this.checkedBoxes = data.Email;
    }

    approve() {
        this.approved = true;

        var obj = { "ID": this.checkedBoxes, "cf": "1" };

        console.log(obj);

        this.httpClient.post(environment.getCollegeVerify, obj)
            .subscribe(
                response => {
                    console.log(response);
                    this.getCollegeStudentData();
                },
                err => {
                    console.log("Error Ocurred" + err);
                }
            )
    }

    loginSubmit(event) {
        const target = event.target;
        const CollegeID = target.querySelector('#login').value;
        const password = target.querySelector('#password').value;
        this.loggedIn = true;

        // if (login === 'colg1' && password === '12345') {
        //   this.loggedIn = true;
        //   console.log(1);
        // } else {
        //   this.invalid = true;
        //   console.log(2);
        // }

        this.login = { "CID": CollegeID };
        this.getCollegeStudentData();
    }

    getCollegeStudentData() {
        this.httpClient.post(environment.getCollegeStudents, this.login)
            .subscribe(
                response => {
                    console.log(response);
                    this.studentData = response;
                },
                err => {
                    console.log("Error Ocurred" + err);
                }
            )
    }
}