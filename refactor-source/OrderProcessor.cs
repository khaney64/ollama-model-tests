using System;
using System.Collections.Generic;
using System.Net.Mail;

namespace LegacyApp
{
    public class OrderProcessor
    {
        // Process the order
        public string ProcessOrder(Dictionary<string, object> order)
        {
            // validate
            if (order == null)
                return "error";

            string customerName = "";
            if (order.ContainsKey("CustomerName"))
                customerName = order["CustomerName"].ToString();

            if (customerName == null || customerName == "")
                return "error: no customer name";

            string email = "";
            if (order.ContainsKey("Email"))
                email = order["Email"].ToString();

            if (email == null || email == "")
                return "error: no email";

            // validate email
            if (!email.Contains("@") || !email.Contains("."))
                return "error: bad email";

            List<Dictionary<string, object>> items = null;
            if (order.ContainsKey("Items"))
                items = (List<Dictionary<string, object>>)order["Items"];

            if (items == null || items.Count == 0)
                return "error: no items";

            // validate items
            for (int i = 0; i < items.Count; i++)
            {
                var item = items[i];
                if (!item.ContainsKey("Name") || !item.ContainsKey("Price") || !item.ContainsKey("Qty"))
                    return "error: invalid item at " + i;

                double price = Convert.ToDouble(item["Price"]);
                int qty = Convert.ToInt32(item["Qty"]);

                if (price <= 0)
                    return "error: bad price";
                if (qty <= 0)
                    return "error: bad qty";
            }

            // calculate totals
            double subtotal = 0;
            for (int i = 0; i < items.Count; i++)
            {
                double p = Convert.ToDouble(items[i]["Price"]);
                int q = Convert.ToInt32(items[i]["Qty"]);
                subtotal += p * q;
            }

            // apply discount
            double discount = 0;
            if (subtotal > 500)
                discount = subtotal * 0.15;
            else if (subtotal > 200)
                discount = subtotal * 0.10;
            else if (subtotal > 100)
                discount = subtotal * 0.05;

            // check if customer is VIP
            bool flag = false;
            if (order.ContainsKey("CustomerType"))
            {
                string tmp = order["CustomerType"].ToString();
                if (tmp == "VIP" || tmp == "vip" || tmp == "Vip")
                    flag = true;
            }

            if (flag)
                discount += subtotal * 0.05;

            double afterDiscount = subtotal - discount;

            // tax
            double tax = 0;
            string state = "";
            if (order.ContainsKey("State"))
                state = order["State"].ToString();

            if (state == "CA")
                tax = afterDiscount * 0.0725;
            else if (state == "NY")
                tax = afterDiscount * 0.08;
            else if (state == "TX")
                tax = afterDiscount * 0.0625;
            else if (state == "FL")
                tax = afterDiscount * 0.06;
            else if (state == "WA")
                tax = afterDiscount * 0.065;
            else
                tax = afterDiscount * 0.05;

            double total = afterDiscount + tax;

            // shipping
            double shipping = 0;
            if (total < 50)
                shipping = 9.99;
            else if (total < 100)
                shipping = 5.99;
            // free shipping over 100

            double x = total + shipping;

            // check inventory
            for (int i = 0; i < items.Count; i++)
            {
                string name = items[i]["Name"].ToString();
                int qty = Convert.ToInt32(items[i]["Qty"]);
                bool inStock = CheckInventory(name, qty);
                if (!inStock)
                    return "error: " + name + " out of stock";
            }

            // update inventory
            for (int i = 0; i < items.Count; i++)
            {
                string name = items[i]["Name"].ToString();
                int qty = Convert.ToInt32(items[i]["Qty"]);
                UpdateInventory(name, qty);
            }

            // save order
            string orderId = Guid.NewGuid().ToString();
            SaveToDatabase(orderId, customerName, x);

            // send email
            try
            {
                SmtpClient client = new SmtpClient("smtp.company.com");
                MailMessage msg = new MailMessage();
                msg.From = new MailAddress("orders@company.com");
                msg.To.Add(email);
                msg.Subject = "Order Confirmation - " + orderId;
                msg.Body = "Dear " + customerName + ",\n\nYour order total is $" + x.ToString("F2") +
                    "\nSubtotal: $" + subtotal.ToString("F2") +
                    "\nDiscount: -$" + discount.ToString("F2") +
                    "\nTax: $" + tax.ToString("F2") +
                    "\nShipping: $" + shipping.ToString("F2") +
                    "\n\nThank you!";
                client.Send(msg);
            }
            catch (Exception)
            {
                // log email failure
                Console.WriteLine("EMAIL FAILED for " + orderId);
            }

            // log
            Console.WriteLine(DateTime.Now.ToString() + " - Order " + orderId + " processed for " + customerName + " - Total: $" + x.ToString("F2"));

            return "success:" + orderId;
        }

        private bool CheckInventory(string itemName, int qty)
        {
            // simulate inventory check
            return true;
        }

        private void UpdateInventory(string itemName, int qty)
        {
            // simulate inventory update
        }

        private void SaveToDatabase(string orderId, string customer, double total)
        {
            // simulate database save
        }

        // duplicate validation that exists in ProcessOrder too
        public bool ValidateEmail(string email)
        {
            if (email == null || email == "")
                return false;
            if (!email.Contains("@"))
                return false;
            if (!email.Contains("."))
                return false;
            return true;
        }

        // another duplicate
        public bool ValidateItems(List<Dictionary<string, object>> items)
        {
            if (items == null || items.Count == 0)
                return false;
            for (int i = 0; i < items.Count; i++)
            {
                var item = items[i];
                if (!item.ContainsKey("Name") || !item.ContainsKey("Price") || !item.ContainsKey("Qty"))
                    return false;
            }
            return true;
        }
    }
}
