# In this code we are creating a pub socket that will generate point on different position
# The positions of the points will be received by subscriber abd displayed on the canvas.
# AS the points change position at every instant.

# Remember to Run the subscriber file first then the publisher
# Remember to change file path as per your path of these files specified in your PC
import zmq
import time
import pandas as pd

csv_file_path = 'C:/Users/omerk/PycharmProjects/QGIS/QGIS_related_Files/selected_rows.csv'
df = pd.read_csv(csv_file_path)

# Initialize ZeroMQ context and socket for publishing
context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://127.0.0.1:1132')

# Group the DataFrame rows based on the TIME column
groups = df.groupby('TIME')

# Infinite loop to continuously publish the data
while True:
    # Iterate over the groups and publish the data
    for time_value, group_df in groups:
        group_csv_data = group_df.to_csv(index=False)
        message = f'{time_value} {group_csv_data}'
        pub_socket.send_string(message)
        print(message)

        # Add some delay
        time.sleep(1)

    # Reset the DataFrame iterator when reaching the end
    groups = df.groupby('TIME')

# Close the ZeroMQ socket and context
pub_socket.close()
context.term()
