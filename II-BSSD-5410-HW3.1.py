from SortFunction import binary_search, merge_sort 
from PixelFunction import compare_pixels, store_pixels, pixels_to_points, grayscale 
from PIL import Image

def main():
    IMG_NAME = 'RGB'
    tolerance = 10  # Default tolerance value
    threshold_color = (255, 0, 0)  # Default threshold color
    
    try:
        with Image.open(IMG_NAME + '.jpg') as im:
            pixels = store_pixels(im)
            print("Stored pixels.")
            
            # Print first few pixels to verify data
            print("First few pixels:", pixels[:10])
            
            # Sort the pixels using merge_sort
            sorted_pixels = pixels.copy()
            merge_sort(sorted_pixels)  # Using merge sort
            print("Sorted pixels.")

            # Convert the sorted pixel list back to an image
            sorted_img = pixels_to_points(im.size, sorted_pixels, mode='RGB')
            sorted_img.save('sorted_' + IMG_NAME + '.jpg', 'JPEG')
            print("Sorted image saved.")

            # Print first few sorted pixels to verify sorting
            print("First few sorted pixels:", sorted_pixels[:10])
            
            # Convert to grayscale
            grayscale_img = im.convert('L')  
            grayscale_pixels = store_pixels(grayscale_img)  # Get grayscale pixel data
            
            # Save the grayscale image
            grayscale_img.save('grayscale_' + IMG_NAME + '.jpg', 'JPEG')
            
            # Enter a loop to handle user input
            while True:
                user_input = input("Enter command (Q to save, R to reverse, T to adjust tolerance, C to change color): ").upper()
                
                if user_input == 'Q':
                    # Highlight pixels that match the threshold color
                    highlighted_positions = {i: px for i, px in enumerate(pixels) if matches_threshold(px, threshold_color, tolerance)}
                    print(f"Highlighted pixels count: {len(highlighted_positions)}")  # Debug print
                    
                    # Create the overlay image by blending grayscale and highlighted pixels
                    final_pixels = [
                        highlighted_positions.get(i, (grayscale_pixels[i], grayscale_pixels[i], grayscale_pixels[i]))
                        for i in range(len(grayscale_pixels))
                    ]
                    
                    final_img = pixels_to_points(im.size, final_pixels, mode='RGB')
                    final_img.save('final_' + IMG_NAME + '.jpg', 'JPEG')
                    print("Final image saved.")
                    
                    break  # Exit the loop after saving

                elif user_input == 'R':
                    # Reverse the order of pixels
                    sorted_pixels.reverse()
                    print("Reversed the sorted pixels.")
                    
                    # Highlight pixels that match the threshold color
                    highlighted_positions = {i: px for i, px in enumerate(sorted_pixels) if matches_threshold(px, threshold_color, tolerance)}
                    print(f"Highlighted pixels count after reverse: {len(highlighted_positions)}")  # Debug print
                    
                    # Create the overlay image
                    overlay_pixels = [highlighted_positions.get(i, (0, 0, 0)) for i in range(len(sorted_pixels))]
                    
                    # Create the overlay image
                    highlighted_img = pixels_to_points(im.size, overlay_pixels, mode='RGB')
                    highlighted_img.show()
                    
                elif user_input == 'T':
                    try:
                        adjustment = int(input("Enter adjustment for tolerance (positive or negative integer): "))
                        tolerance = max(0, tolerance + adjustment)
                        print(f"Adjusted tolerance to: {tolerance}")

                        # Update the highlighted pixels based on the new tolerance
                        highlighted_positions = {i: px for i, px in enumerate(pixels) if matches_threshold(px, threshold_color, tolerance)}
                        print(f"Highlighted pixels count after tolerance adjustment: {len(highlighted_positions)}")  # Debug print
                        
                        overlay_pixels = [highlighted_positions.get(i, (0, 0, 0)) for i in range(len(pixels))]
                        
                        # Create the overlay image
                        highlighted_img = pixels_to_points(im.size, overlay_pixels, mode='RGB')
                        highlighted_img.show()
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")

                elif user_input == 'C':
                    try:
                        r = int(input("Enter R value (0-255): "))
                        g = int(input("Enter G value (0-255): "))
                        b = int(input("Enter B value (0-255): "))
                        if not (0 <= r <= 255 and not 0 <= g <= 255 and not 0 <= b <= 255):
                            raise ValueError("RGB values must be between 0 and 255.")
                        threshold_color = (r, g, b)
                        print(f"New color to highlight: {threshold_color}")

                        # Update the highlighted pixels based on the new color
                        highlighted_positions = {i: px for i, px in enumerate(pixels) if matches_threshold(px, threshold_color, tolerance)}
                        print(f"Highlighted pixels count after color change: {len(highlighted_positions)}")  # Debug print
                        
                        overlay_pixels = [highlighted_positions.get(i, (0, 0, 0)) for i in range(len(pixels))]
                        
                        # Create the overlay image
                        highlighted_img = pixels_to_points(im.size, overlay_pixels, mode='RGB')
                        highlighted_img.show()
                    except ValueError as e:
                        print(f"Invalid input. Please enter valid RGB values (0-255). Error: {e}")

                else:
                    print("Invalid command. Please enter Q, R, T, or C.")
                    
    except FileNotFoundError:
        print(f"File '{IMG_NAME}.jpg' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def matches_threshold(pixel, threshold_color, tolerance=10):
    """Check if a pixel is within the tolerance range of the threshold color."""
    r, g, b = pixel
    t_r, t_g, t_b = threshold_color
    return (abs(r - t_r) < tolerance) and (abs(g - t_g) < tolerance) and (abs(b - t_b) < tolerance)

if __name__ == "__main__":
    main()
