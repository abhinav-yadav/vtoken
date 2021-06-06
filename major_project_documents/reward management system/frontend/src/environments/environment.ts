// This file can be replaced during build by using the `fileReplacements` array.
// `ng build ---prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  getUnverifiedStudentsData: 'http://localhost:3000/unverifiedstudents',
  getVerifiedStudentsData: 'http://localhost:3000/verifiedstudents',
  postStudentForConfirmation: 'http://localhost:3000/universityverify',
  getCollegeStudents: 'http://localhost:3000/collegestudents',
  getCollegeVerify: 'http://localhost:3000/collegeverify',
  getStudent: 'http://localhost:3000/getStudent',
  verifyStudent: 'http://localhost:3000/studentverify',
  validate: 'http://localhost:3000/validate',
  addStudent: 'http://localhost:3000/createcertificate'
};
