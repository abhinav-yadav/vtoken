import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
    selector: 'app-addStudent',
    templateUrl: './addStudent.component.html',
    styleUrls: ['./addStudent.component.css']
})
export class AddStudent {

    studentData;
    studentName;
    studentBranch;
    passingYear;
    collegeID;
    degree;
    approved = false;
    succesfullSubmission = false;
    beforeSubmission = true;
    studentObj;
    alreadyConfirmed = false;

    studentForm = new FormGroup({
        studentName: new FormControl(),
        studentBranch: new FormControl(),
        passingYear: new FormControl(),
        degree: new FormControl(),
        collegeID: new FormControl(),
        email: new FormControl()
    });

    constructor(private fb: FormBuilder, private httpClient: HttpClient) {
        this.createForm();
    }

    createForm() {
        this.studentForm = this.fb.group({
            studentName: ['', Validators.required],
            studentBranch: ['', Validators.required],
            passingYear: ['', Validators.required],
            degree: ['', Validators.required],
            collegeID: ['', Validators.required],
            email: ['', Validators.required],
        });
    }

    submitDetails(event) {
        const target = event.target;
        const studentName = target.querySelector('#studentName').value;
        const studentBranch = target.querySelector('#studentBranch').value;
        const passingYear = target.querySelector('#passingYear').value;
        const degree = target.querySelector('#degree').value;
        const collegeID = target.querySelector('#collegeID').value;
        const email = target.querySelector('#email').value;

        this.succesfullSubmission = true;
        this.beforeSubmission = false;


        this.studentObj = { "collegeID": collegeID, "email": email, "name": studentName, "branch": studentBranch, "year": passingYear, "Degree": degree };

        console.log(this.studentObj);

        this.httpClient.post(environment.addStudent, this.studentObj)
            .subscribe(
                response => {
                    console.log(response);
                    this.approved = true;
                },
                err => {
                    console.log("Error Ocurred" + err);
                }
            )
    }

}