
def delete_invalid_reservations(reservations):
    for reservation in reservations:
        if reservation.time_has_ended():
            reservation.delete()
