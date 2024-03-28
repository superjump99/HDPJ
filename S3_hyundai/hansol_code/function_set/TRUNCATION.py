from math import pi
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# Re-plotting with the corrected reference to pi

pentagon_coords = [(-2, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-2, 0)]



# Plotting
fig, ax = plt.subplots()

# Plot pentagon
pentagon = plt.Polygon(pentagon_coords, closed=True, edgecolor='r', fill=False)
ax.add_patch(pentagon)

# Plot each box with rotation
for box in boxes:
    angle = radians(box["rotationYaw"])  # Convert to radians
    # Create a rectangle patch with bottom left at (x, y), but it needs to be rotated about its center
    rect = patches.Rectangle((box["x"] - box["width"]/2, box["y"] - box["length"]/2), box["width"], box["length"], angle=angle * 180/pi, linewidth=1, edgecolor='b', facecolor='none')
    # Apply the rotation
    t = patches.transforms.Affine2D().rotate_around(box["x"], box["y"], angle) + ax.transData
    rect.set_transform(t)
    ax.add_patch(rect)

# Setting the aspect ratio to equal to make sure the scale is not distorted
ax.set_aspect('equal')
plt.xlim(-10, 130)
plt.ylim(-60, 60)
plt.show()