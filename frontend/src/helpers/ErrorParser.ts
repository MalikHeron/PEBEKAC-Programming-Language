import { FirebaseError } from 'firebase/app';

export class ErrorParser {
   static errorMap: { [key: string]: string } = {
      "auth/invalid-email": "Email is invalid.",
      "auth/invalid-credential": "Invalid email or password.",
      "auth/invalid-verification-code": "Invalid verification code.",
      "auth/user-not-found": "User not found.",
      "auth/invalid-login-credentials": "Invalid login credentials",
      "auth/wrong-password": "The Password is incorrect.",
      "auth/user-disabled": "User is disabled.",
      "auth/too-many-requests": "Too many requests. Please try again later.",
      "auth/email-already-in-use": "Email already in use. Try signing in.",
      "auth/weak-password": "Your Password is too weak.",
      "operation-not-allowed": "Operation not allowed.",
      "firestore/insufficient-permission": "You don't have permission to do that.",
   };

   static parse(error) {
      let text = "";

      if (error instanceof FirebaseError) {
         console.log(error.code);
         text = this.errorMap[error.code as string];
      }

      if (text != "" && text != undefined) {
         return text;
      }

      return "Something went wrong. Try again later.";
   }
}
