import { Timestamp } from "firebase/firestore";

/**
 * A utility class for formatting timestamps and dates.
 */
export class DateFormatter {
   /**
   * Formats a timestamp into a human-readable date format.
   * @param {Timestamp} timestamp - The timestamp to format.
   * @returns {string} - The formatted date string.
   */
   static formatTimestampToRelativeDate(timestamp: Timestamp): string {
      const date = new Date(timestamp.seconds * 1000);
      const today = new Date();
      const yesterday = new Date(today.getTime());
      yesterday.setDate(yesterday.getDate() - 1);

      // If the date is today, return the time
      if (date.toDateString() === today.toDateString()) {
         return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
      }
      // If the date was yesterday, return 'Yesterday'
      else if (date.toDateString() === yesterday.toDateString()) {
         return 'Yesterday';
      }
      // If the date was within the last 6 days, return the number of days ago
      else if (date.getTime() > today.getTime() - 6 * 24 * 60 * 60 * 1000) {
         const diffTime = Math.abs(today.getTime() - date.getTime());
         const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
         return `${diffDays} days ago`;
      }
      // Otherwise, return the date in 'Dec 23, 2023' format
      else {
         return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
      }
   }

   /**
    * Converts a date string to a Firestore Timestamp.
    * @param {string} dateString - The date string to convert.
    * @returns {Timestamp} - The converted Timestamp.
    */
   static convertDateToTimestamp(dateString: string): Timestamp {
      const date = new Date(dateString);
      return Timestamp.fromDate(date);
   }

   /**
    * Converts a Firestore Timestamp to a date string.
    * @param {Timestamp} timestamp - The Firestore Timestamp to convert.
    * @returns {string} - The converted date string.
    */
   static convertTimestampToDate(timestamp: Timestamp | undefined): string {
      if (timestamp === undefined) {
         return '';
      }
      const date = timestamp.toDate();
      const year = date.getFullYear();
      const month = ("0" + (date.getMonth() + 1)).slice(-2); // Months are 0-based in JavaScript
      const day = ("0" + date.getDate()).slice(-2);
      return `${year}-${month}-${day}`; // Returns date string in 'YYYY-MM-DD' format
   }

   /**
 * Converts a Firestore Timestamp to a date string.
 * @param {Timestamp} timestamp - The Firestore Timestamp to convert.
 * @returns {string} - The converted date string.
 */
   static convertTimestampToAmericanDate(timestamp: Timestamp | undefined): string {
      if (timestamp === undefined) {
         return '';
      }
      const date = timestamp.toDate();
      const year = date.getFullYear();
      const monthNames = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"];
      const month = monthNames[date.getMonth()]; // Months are 0-based in JavaScript
      const day = date.getDate();
      return `${month} ${day}, ${year}`; // Returns date string in 'Month Day, Year' format
   }
}