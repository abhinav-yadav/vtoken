import { Component } from '@angular/core';
import { FormControl, FormGroup, FormBuilder, Validators, NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';

@Component({
  selector: 'app-university',
  templateUrl: './university.component.html',
  styleUrls: ['./university.component.css']
})
export class UniversityComponent {
  title = 'app';
  formSubmitted = false;
  submit;
  loggedIn;
  invalid;
  studentData;
  forVerificationData;
  checkedBoxes = [];
  uncheckedData = [];

  angularForm = new FormGroup({
  });

  form = new FormGroup({
    login: new FormControl(),
    password: new FormControl()
  });

  constructor(private fb: FormBuilder, private httpClient: HttpClient, private routes: Router) {
    this.createForm();
  }

  createForm() {
    this.form = this.fb.group({
      login: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  refresh() {
    window.location.reload();
  }

  ngOnInit() {
    this.loggedIn = false;
    this.invalid = false;
    this.submit = false;
  }

  loginSubmit(event) {
    const target = event.target;
    const login = target.querySelector('#login').value;
    const password = target.querySelector('#password').value;
    this.loggedIn = true;

    // if (login === 'univ1' && password === '12345') {
    //   this.loggedIn = true;
    //   console.log(1);
    // } else {
    //   this.invalid = true;
    //   console.log(2);
    // }

    //Get data of all unverified students
    this.httpClient.get(environment.getUnverifiedStudentsData)
      .subscribe(
        response => {
          this.studentData = response;
        },
        err => {
          console.log("Error Ocurred" + err);
        }
      )

    this.getVerifiedStudent();
  }

  checkboxClicked(data) {
    this.checkedBoxes.push(data.ID);
    this.uncheckedData.push(data);
  }

  sendDataForConfirmation() {

    var obj = [];
    var i;

    for (i = 0; i < this.checkedBoxes.length; i++) {
      obj[i] = { "ID": this.checkedBoxes[i] };
    }
    console.log(obj);

    this.httpClient.post(environment.postStudentForConfirmation, obj)
      .subscribe(
        response => {
          console.log(response);

          this.studentData = response;
          this.getVerifiedStudent();

        },
        err => {
          console.log("Error Ocurred" + err);
        }
      )
  }

  getVerifiedStudent() {
    return this.httpClient.get(environment.getVerifiedStudentsData)
      .subscribe(
        response => {
          this.forVerificationData = response;
        },
        err => {
          console.log("Error Ocurred" + err);
        }
      )
  }
}
