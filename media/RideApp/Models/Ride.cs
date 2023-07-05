using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RideApp.Models
{
    public class Ride
    {
        public int Id { get; set; }
        public string StartLocation { get; set; }
        public string EndLocation { get; set; }
        public DateTime RideDate { get; set; }
        public string CarModel { get; set; }
        public string PassengerName { get; set; }
        public string DriverName { get; set; }
        public string Status { get; set; }
        public DateTime ReservationDate { get; set; }
    }
}
