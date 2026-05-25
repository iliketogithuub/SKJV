#!/usr/bin/env python3
import os
import glob
import subprocess
import sys

def translate_all():
    source_dir = "/home/charlie/Downloads/kjv-markdown-master"
    target_dir = "/home/charlie/Desktop/Websites/SKJV/books"
    script_dir = "/home/charlie/Desktop/Websites/SKJV/scripts"
    
    translate_script = os.path.join(script_dir, "translate_kjv_to_skjv.py")
    verify_script = os.path.join(script_dir, "verify_translation.py")
    
    # Find all source files
    pattern = os.path.join(source_dir, "[0-9][0-9] - * - KJV.md")
    source_files = sorted(glob.glob(pattern))
    
    if not source_files:
        print("No KJV markdown files found in the source directory!")
        sys.exit(1)
        
    print(f"Found {len(source_files)} books to translate.")
    
    success_count = 0
    fail_count = 0
    
    for src in source_files:
        filename = os.path.basename(src)
        # Construct target name: e.g. "01 - Genesis - SKJV.md"
        target_filename = filename.replace("- KJV.md", "- SKJV.md")
        tgt = os.path.join(target_dir, target_filename)
        
        print(f"\n==========================================")
        print(f"Translating: {filename}")
        print(f"==========================================")
        
        # Run translation script
        cmd = [sys.executable, translate_script, "--source", src, "--target", tgt]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode == 0:
            print(f"Translation complete: {target_filename}")
            
            # Run verification script
            v_cmd = [sys.executable, verify_script, tgt]
            v_res = subprocess.run(v_cmd, capture_output=True, text=True)
            
            print(v_res.stdout)
            if v_res.returncode == 0:
                success_count += 1
            else:
                print(v_res.stderr)
                fail_count += 1
        else:
            print(f"FAIL translating: {filename}")
            print(res.stderr)
            fail_count += 1
            
    print("\n==========================================")
    print("TRANSLATION SUMMARY")
    print(f"Total Books: {len(source_files)}")
    print(f"Successful & Verified: {success_count}")
    print(f"Failed/Validation Errors: {fail_count}")
    print("==========================================")
    
if __name__ == "__main__":
    translate_all()
