using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace InventoryMid.Models
{
    public class Inventory
    {
        public string productName { get; set; }
        public int productCode { get; set; }
        public string category { get; set; }
        public string productDescription { get; set; }
        public int price { get; set; }
        public string warehouse { get; set; }
        public string vendor { get; set; }
        public string quantity { get; set; }
        
    }
}
