seconds = 1
meters = 1
pixels = 1


class vals:
    normalize = True
    trail = True
    trails = []
    trail_length = 500

    screen_size: pixels = 600

    pixel_scale: pixels/meters = 7e-7
    meters_transpose: meters = screen_size / 2 / pixel_scale

    center_x: pixels = screen_size / 2
    center_y: pixels = screen_size / 2

    time_per_iter: seconds = .01
    simulation_seconds_per_iter: seconds = 1
    dT: seconds = .0001
