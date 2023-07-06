using Microsoft.EntityFrameworkCore;
using RideApp.Models;

public class RideReservationDbContext : DbContext
{
    public DbSet<Ride> Rides { get; set; }

    public RideReservationDbContext(DbContextOptions<RideReservationDbContext> options) : base(options)
    {
        Database.EnsureCreated();
    }
}
