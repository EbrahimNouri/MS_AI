#!/usr/bin/env python3
"""
Simple Pathlib Demo Application
A practical example of using pathlib for file system operations
"""

from pathlib import Path
import datetime
import json
import os


class SimpleFileManager:
    """A simple file manager using pathlib"""

    def __init__(self, base_dir=None):
        """Initialize with a base directory"""
        if base_dir is None:
            self.base_dir = Path.cwd()
        else:
            self.base_dir = Path(base_dir)

        # Ensure the base directory exists
        self.base_dir.mkdir(exist_ok=True)
        print(f"📁 Working directory: {self.base_dir}")

    def create_file(self, filename, content=""):
        """Create a new file with optional content"""
        file_path = self.base_dir / filename
        try:
            file_path.write_text(content)
            print(f"✅ Created: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return None

    def read_file(self, filename):
        """Read content from a file"""
        file_path = self.base_dir / filename
        if file_path.exists() and file_path.is_file():
            try:
                content = file_path.read_text()
                print(f"📖 Read: {file_path}")
                return content
            except Exception as e:
                print(f"❌ Error reading file: {e}")
                return None
        else:
            print(f"❌ File not found: {file_path}")
            return None

    def create_directory(self, dirname):
        """Create a new directory"""
        dir_path = self.base_dir / dirname
        try:
            dir_path.mkdir(exist_ok=True)
            print(f"📁 Created directory: {dir_path}")
            return dir_path
        except Exception as e:
            print(f"❌ Error creating directory: {e}")
            return None

    def list_files(self, pattern="*"):
        """List all files in the base directory matching a pattern"""
        files = list(self.base_dir.glob(pattern))
        files = [f for f in files if f.is_file()]

        if files:
            print(f"\n📋 Files in {self.base_dir}:")
            for file in files:
                size = file.stat().st_size
                modified = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                print(
                    f"  📄 {file.name} ({size} bytes, modified: {modified.strftime('%Y-%m-%d %H:%M')})"
                )
        else:
            print(f"📋 No files found in {self.base_dir}")

        return files

    def list_directories(self):
        """List all directories in the base directory"""
        dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]

        if dirs:
            print(f"\n📂 Directories in {self.base_dir}:")
            for dir_path in dirs:
                print(f"  📂 {dir_path.name}")
        else:
            print(f"📂 No directories found in {self.base_dir}")

        return dirs

    def copy_file(self, source, destination):
        """Copy a file from source to destination"""
        source_path = self.base_dir / source
        dest_path = self.base_dir / destination

        if not source_path.exists():
            print(f"❌ Source file not found: {source_path}")
            return None

        try:
            dest_path.write_bytes(source_path.read_bytes())
            print(f"📋 Copied: {source_path} -> {dest_path}")
            return dest_path
        except Exception as e:
            print(f"❌ Error copying file: {e}")
            return None

    def move_file(self, source, destination):
        """Move (rename) a file"""
        source_path = self.base_dir / source
        dest_path = self.base_dir / destination

        if not source_path.exists():
            print(f"❌ Source file not found: {source_path}")
            return None

        try:
            source_path.rename(dest_path)
            print(f"↔️  Moved: {source_path} -> {dest_path}")
            return dest_path
        except Exception as e:
            print(f"❌ Error moving file: {e}")
            return None

    def delete_file(self, filename):
        """Delete a file"""
        file_path = self.base_dir / filename
        if file_path.exists() and file_path.is_file():
            try:
                file_path.unlink()
                print(f"🗑️  Deleted: {file_path}")
                return True
            except Exception as e:
                print(f"❌ Error deleting file: {e}")
                return False
        else:
            print(f"❌ File not found: {file_path}")
            return False

    def get_file_info(self, filename):
        """Get detailed information about a file"""
        file_path = self.base_dir / filename

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return None

        stats = file_path.stat()
        info = {
            "name": file_path.name,
            "path": str(file_path),
            "parent": str(file_path.parent),
            "exists": file_path.exists(),
            "is_file": file_path.is_file(),
            "is_dir": file_path.is_dir(),
            "size_bytes": stats.st_size,
            "created": datetime.datetime.fromtimestamp(stats.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "modified": datetime.datetime.fromtimestamp(stats.st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "accessed": datetime.datetime.fromtimestamp(stats.st_atime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "extension": file_path.suffix,
            "stem": file_path.stem,
            "absolute": str(file_path.absolute()),
        }

        print(f"\n📊 File information for: {file_path.name}")
        for key, value in info.items():
            print(f"  {key}: {value}")

        return info

    def find_files_by_extension(self, extension):
        """Find all files with a specific extension"""
        pattern = f"*{extension}"
        files = list(self.base_dir.rglob(pattern))
        files = [f for f in files if f.is_file()]

        if files:
            print(f"\n🔍 Found {len(files)} files with extension '{extension}':")
            for file in files:
                print(f"  📄 {file}")
        else:
            print(f"🔍 No files found with extension '{extension}'")

        return files

    def create_sample_structure(self):
        """Create a sample file structure for demonstration"""
        print("\n🏗️  Creating sample file structure...")

        # Create directories
        self.create_directory("docs")
        self.create_directory("data")
        self.create_directory("backup")

        # Create sample files
        self.create_file(
            "README.md", "# Sample Project\n\nThis is a demonstration of pathlib."
        )
        self.create_file(
            "config.json", '{"app_name": "Pathlib Demo", "version": "1.0.0"}'
        )
        self.create_file("data/sample.txt", "This is a sample text file.")
        self.create_file("docs/guide.txt", "Here's the user guide.")

        # Create a JSON file with structured data
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": os.getenv("USER", "unknown"),
            "files": ["README.md", "config.json"],
        }
        self.create_file("data/info.json", json.dumps(data, indent=2))

        print("✅ Sample structure created!\n")


def main():
    """Main function to demonstrate the app"""
    print("=" * 60)
    print("  PATHLIB FILE MANAGER - Simple Python App")
    print("=" * 60 + "\n")

    # Initialize the file manager
    app = SimpleFileManager()

    # Create sample structure
    app.create_sample_structure()

    # List current files and directories
    app.list_files()
    app.list_directories()

    # Demonstrate various operations
    print("\n" + "=" * 60)
    print("  DEMONSTRATING PATHLIB OPERATIONS")
    print("=" * 60)

    # 1. Create a new file
    app.create_file("hello.txt", "Hello, world!\nThis is created with pathlib.")

    # 2. Read a file
    content = app.read_file("README.md")
    if content:
        print(f"Content preview: {content[:100]}...")

    # 3. Get file information
    app.get_file_info("config.json")

    # 4. Copy a file
    app.copy_file("config.json", "backup/config_backup.json")

    # 5. Find files by extension
    app.find_files_by_extension(".txt")
    app.find_files_by_extension(".json")

    # 6. List all files after operations
    app.list_files()

    # 7. Move/rename a file
    app.move_file("hello.txt", "greeting.txt")

    # 8. Check final structure
    print("\n" + "=" * 60)
    print("  FINAL FILE STRUCTURE")
    print("=" * 60)

    # Recursively list all files
    all_files = list(app.base_dir.rglob("*"))
    for file in sorted(all_files):
        if file.is_file():
            rel_path = file.relative_to(app.base_dir)
            print(f"  📄 {rel_path}")
        elif file.is_dir():
            rel_path = file.relative_to(app.base_dir)
            print(f"  📁 {rel_path}/")

    # 9. Optional: Clean up (commented out for demo)
    # If you want to clean up the created files, uncomment:
    # print("\n🧹 Cleaning up...")
    # for file in all_files:
    #     if file.is_file():
    #         file.unlink()
    # for dir in [d for d in app.base_dir.iterdir() if d.is_dir()]:
    #     dir.rmdir()
    # print("✅ Cleanup complete!")

    print("\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
