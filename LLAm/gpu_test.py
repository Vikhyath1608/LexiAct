import torch
import subprocess

# Check if GPU is available
def list_gpus():
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        for i in range(gpu_count):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("No GPU available.")

# List CPU info
def list_cpu():
    try:
        # Use subprocess to get detailed CPU info (works on Unix-based systems)
        cpu_info = subprocess.check_output("lscpu", shell=True).strip().decode()
        print("CPU Information:\n", cpu_info)
    except Exception as e:
        # Fallback for Windows or systems without 'lscpu'
        print("CPU Information:")
        print(f"Number of CPUs: {torch.get_num_threads()} (Threads)")

if __name__ == "__main__":
    print("Listing available hardware:")
    list_cpu()
    list_gpus()
