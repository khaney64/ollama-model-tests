using System;
using System.Collections.Generic;
using System.IO;

namespace LegacyApp
{
    public class ReportGenerator
    {
        // Generate report - supports multiple formats
        public string GenerateReport(string reportType, string format, DateTime startDate, DateTime endDate,
            string department, bool includeInactive, string sortBy, string outputPath)
        {
            // get data
            var data = GetReportData(reportType, startDate, endDate, department, includeInactive);

            if (data == null || data.Count == 0)
                return "No data found";

            // sort data
            if (sortBy == "name")
                data.Sort((a, b) => a["Name"].ToString().CompareTo(b["Name"].ToString()));
            else if (sortBy == "date")
                data.Sort((a, b) => Convert.ToDateTime(a["Date"]).CompareTo(Convert.ToDateTime(b["Date"])));
            else if (sortBy == "amount")
                data.Sort((a, b) => Convert.ToDouble(a["Amount"]).CompareTo(Convert.ToDouble(b["Amount"])));

            string result = "";

            // This switch should really be polymorphism
            switch (format.ToLower())
            {
                case "html":
                    result = "<html><head><title>" + reportType + " Report</title>";
                    result += "<style>table { border-collapse: collapse; } td, th { border: 1px solid black; padding: 5px; }</style>";
                    result += "</head><body>";
                    result += "<h1>" + reportType + " Report</h1>";
                    result += "<p>Period: " + startDate.ToString("yyyy-MM-dd") + " to " + endDate.ToString("yyyy-MM-dd") + "</p>";
                    result += "<p>Department: " + department + "</p>";
                    result += "<table><tr><th>Name</th><th>Date</th><th>Amount</th><th>Status</th></tr>";
                    for (int i = 0; i < data.Count; i++)
                    {
                        result += "<tr>";
                        result += "<td>" + data[i]["Name"] + "</td>";
                        result += "<td>" + data[i]["Date"] + "</td>";
                        result += "<td>$" + Convert.ToDouble(data[i]["Amount"]).ToString("F2") + "</td>";
                        result += "<td>" + data[i]["Status"] + "</td>";
                        result += "</tr>";
                    }
                    result += "</table>";
                    // Calculate total
                    double htmlTotal = 0;
                    for (int i = 0; i < data.Count; i++)
                        htmlTotal += Convert.ToDouble(data[i]["Amount"]);
                    result += "<p><strong>Total: $" + htmlTotal.ToString("F2") + "</strong></p>";
                    result += "</body></html>";
                    break;

                case "csv":
                    result = "Name,Date,Amount,Status\n";
                    for (int i = 0; i < data.Count; i++)
                    {
                        result += data[i]["Name"] + "," + data[i]["Date"] + "," + data[i]["Amount"] + "," + data[i]["Status"] + "\n";
                    }
                    // Calculate total for csv too
                    double csvTotal = 0;
                    for (int i = 0; i < data.Count; i++)
                        csvTotal += Convert.ToDouble(data[i]["Amount"]);
                    result += "TOTAL,," + csvTotal.ToString("F2") + ",\n";
                    break;

                case "text":
                    result = "=== " + reportType + " Report ===\n";
                    result += "Period: " + startDate.ToString("yyyy-MM-dd") + " to " + endDate.ToString("yyyy-MM-dd") + "\n";
                    result += "Department: " + department + "\n\n";
                    for (int i = 0; i < data.Count; i++)
                    {
                        result += data[i]["Name"] + " | " + data[i]["Date"] + " | $" + Convert.ToDouble(data[i]["Amount"]).ToString("F2") + " | " + data[i]["Status"] + "\n";
                    }
                    double textTotal = 0;
                    for (int i = 0; i < data.Count; i++)
                        textTotal += Convert.ToDouble(data[i]["Amount"]);
                    result += "\nTotal: $" + textTotal.ToString("F2") + "\n";
                    break;

                case "json":
                    result = "{ \"report\": \"" + reportType + "\", \"data\": [";
                    for (int i = 0; i < data.Count; i++)
                    {
                        if (i > 0) result += ",";
                        result += "{ \"name\": \"" + data[i]["Name"] + "\", \"date\": \"" + data[i]["Date"] + "\", \"amount\": " + data[i]["Amount"] + ", \"status\": \"" + data[i]["Status"] + "\" }";
                    }
                    result += "] }";
                    break;

                default:
                    return "Unknown format: " + format;
            }

            // save to file - hardcoded path
            try
            {
                string fullPath = "C:\\Reports\\" + outputPath;
                File.WriteAllText(fullPath, result);
            }
            catch (Exception ex)
            {
                // swallow exception
            }

            // This method was supposed to send an email but we removed that feature
            // SendReportEmail(result, department);
            // TODO: re-enable email notifications
            // string emailResult = PrepareEmailBody(result);
            // if (emailResult != null && emailResult != "") { ... }

            return result;
        }

        // This method is never called anymore - dead code
        private string PrepareEmailBody(string content)
        {
            string body = "<html><body>";
            body += "<p>Please find the attached report.</p>";
            body += content;
            body += "</body></html>";
            return body;
        }

        // Misleading comment: this does NOT validate the report
        // It actually just checks if the type is supported
        private bool ValidateReport(string type)
        {
            if (type == "sales" || type == "inventory" || type == "employees" || type == "expenses")
                return true;
            return false;
        }

        private List<Dictionary<string, object>> GetReportData(string type, DateTime start, DateTime end,
            string dept, bool includeInactive)
        {
            // Simulate fetching data
            var result = new List<Dictionary<string, object>>();
            result.Add(new Dictionary<string, object> {
                { "Name", "Item 1" }, { "Date", "2024-01-15" },
                { "Amount", 150.00 }, { "Status", "Active" }
            });
            result.Add(new Dictionary<string, object> {
                { "Name", "Item 2" }, { "Date", "2024-02-20" },
                { "Amount", 275.50 }, { "Status", "Active" }
            });
            result.Add(new Dictionary<string, object> {
                { "Name", "Item 3" }, { "Date", "2024-03-10" },
                { "Amount", 89.99 }, { "Status", "Inactive" }
            });
            return result;
        }
    }
}
