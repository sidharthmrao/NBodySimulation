seconds = 1
meters = 1
pixels = 1


class vals:
    normalize = True  # Whether to normalize the velocity vectors appearance
    trail = True  # Whether to draw trails
    trails = []  # List of trails
    trail_length = 500  # Length of trails

    screen_size: pixels = 600  # Size of the screen in pixels

    pixel_scale: pixels/meters = 7e-7  # How many pixels per meter
    meters_transpose: meters = screen_size / 2 / pixel_scale  # How many meters per pixel

    center_x: pixels = screen_size / 2  # Center of the screen in pixels
    center_y: pixels = screen_size / 2

    time_per_iter: seconds = .01  # How many seconds per iteration
    simulation_seconds_per_iter: seconds = 1  # How many real time seconds to simulate per iteration
    dT: seconds = .0001  # Precision of the simulation

    frames_per_second = 30
    simulation_seconds_per_real_second = 1
