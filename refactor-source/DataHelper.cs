using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.IO;

namespace LegacyApp
{
    // Utility class for data operations
    public static class DataHelper
    {
        private static string connStr = "Server=localhost;Database=AppDB;Trusted_Connection=true;";

        // Get user by ID
        public static Dictionary<string, object> GetUser(int id, bool IncludeAddress, bool includeOrders)
        {
            try
            {
                using (var conn = new SqlConnection(connStr))
                {
                    conn.Open();
                    var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = " + id, conn);
                    var reader = cmd.ExecuteReader();
                    if (reader.Read())
                    {
                        var user = new Dictionary<string, object>();
                        user["Id"] = reader["Id"];
                        user["name"] = reader["Name"];
                        user["EMAIL"] = reader["Email"];
                        user["phone"] = reader["Phone"];

                        if (IncludeAddress)
                        {
                            reader.Close();
                            var cmd2 = new SqlCommand("SELECT * FROM Addresses WHERE UserId = " + id, conn);
                            var reader2 = cmd2.ExecuteReader();
                            if (reader2.Read())
                            {
                                user["street"] = reader2["Street"];
                                user["city"] = reader2["City"];
                                user["State"] = reader2["State"];
                                user["ZIP"] = reader2["Zip"];
                            }
                        }

                        if (includeOrders)
                        {
                            reader.Close();
                            var cmd3 = new SqlCommand("SELECT * FROM Orders WHERE CustomerId = " + id, conn);
                            var reader3 = cmd3.ExecuteReader();
                            var orders = new List<Dictionary<string, object>>();
                            while (reader3.Read())
                            {
                                var o = new Dictionary<string, object>();
                                o["OrderId"] = reader3["Id"];
                                o["total"] = reader3["Total"];
                                o["Date"] = reader3["OrderDate"];
                                orders.Add(o);
                            }
                            user["orders"] = orders;
                        }

                        return user;
                    }
                }
            }
            catch (Exception)
            {
                return null;
            }
            return null;
        }

        // Read config from file
        public static string ReadConfig(string key)
        {
            try
            {
                string[] lines = File.ReadAllLines("C:\\App\\config.txt");
                for (int i = 0; i < lines.Length; i++)
                {
                    string[] parts = lines[i].Split('=');
                    if (parts.Length == 2 && parts[0].Trim() == key)
                        return parts[1].Trim();
                }
            }
            catch (Exception)
            {
                return null;
            }
            return null;
        }

        // Read config from file - copy pasted with minor change
        public static string ReadConfigWithDefault(string key, string defaultValue)
        {
            try
            {
                string[] lines = File.ReadAllLines("C:\\App\\config.txt");
                for (int i = 0; i < lines.Length; i++)
                {
                    string[] parts = lines[i].Split('=');
                    if (parts.Length == 2 && parts[0].Trim() == key)
                        return parts[1].Trim();
                }
            }
            catch (Exception)
            {
                return defaultValue;
            }
            return defaultValue;
        }

        // format date - why is this even here?
        public static string FormatDate(DateTime dt, bool includeTime)
        {
            if (includeTime)
                return dt.ToString("yyyy-MM-dd HH:mm:ss");
            else
                return dt.ToString("yyyy-MM-dd");
        }

        // format currency
        public static string formatCurrency(double amount)
        {
            return "$" + amount.ToString("F2");
        }

        // format currency with symbol parameter - copy paste again
        public static string formatCurrency(double amount, string symbol)
        {
            return symbol + amount.ToString("F2");
        }

        // log to file
        public static void LogMessage(string message)
        {
            try
            {
                File.AppendAllText("C:\\Logs\\app.log",
                    DateTime.Now.ToString() + " - " + message + "\n");
            }
            catch (Exception)
            {
                // silently fail
            }
        }

        // log error to file - almost identical to LogMessage
        public static void logError(string message)
        {
            try
            {
                File.AppendAllText("C:\\Logs\\error.log",
                    DateTime.Now.ToString() + " - ERROR - " + message + "\n");
            }
            catch (Exception)
            {
                // silently fail
            }
        }

        // check if string is a number
        public static bool isNumeric(string str)
        {
            double result;
            return double.TryParse(str, out result);
        }

        // check if string is a valid email - duplicated from OrderProcessor!
        public static bool IsValidEmail(string email)
        {
            if (email == null || email == "")
                return false;
            if (!email.Contains("@"))
                return false;
            if (!email.Contains("."))
                return false;
            return true;
        }

        // convert list to CSV string
        public static string ListToCsv(List<string> items)
        {
            string result = "";
            for (int i = 0; i < items.Count; i++)
            {
                if (i > 0) result += ",";
                result += items[i];
            }
            return result;
        }

        // parse CSV string to list - why not just use Split?
        public static List<string> CsvToList(string csv)
        {
            var result = new List<string>();
            string current = "";
            for (int i = 0; i < csv.Length; i++)
            {
                if (csv[i] == ',')
                {
                    result.Add(current);
                    current = "";
                }
                else
                {
                    current += csv[i];
                }
            }
            if (current != "")
                result.Add(current);
            return result;
        }
    }
}
