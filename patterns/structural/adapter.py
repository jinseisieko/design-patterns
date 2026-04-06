"""Adapter Pattern Demonstration (C++).

Real-world context: Media player supporting legacy audio formats (VLC, MP4)
by adapting them to a common MediaPlayer interface.

Anti-pattern warning: Over-Abstraction - Creating adapters for systems that
are already compatible, introducing unnecessary indirection.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Target Interface
class MediaPlayer {
public:
    virtual void play(const std::string& type, const std::string& file) = 0;
    virtual ~MediaPlayer() = default;
};

// Adaptee: Legacy Advanced Media Player
class AdvancedMediaPlayer {
public:
    virtual void playVlc(const std::string& file) = 0;
    virtual void playMp4(const std::string& file) = 0;
};

// Concrete Adaptee: VLC Player
class VlcPlayer : public AdvancedMediaPlayer {
public:
    void playVlc(const std::string& file) override {
        std::cout << "Playing VLC: " << file << "\n";
    }
    void playMp4(const std::string&) override {}
};

// Concrete Adaptee: MP4 Player
class Mp4Player : public AdvancedMediaPlayer {
public:
    void playVlc(const std::string&) override {}
    void playMp4(const std::string& file) override {
        std::cout << "Playing MP4: " << file << "\n";
    }
};

// Adapter
class MediaAdapter : public MediaPlayer {
private:
    std::unique_ptr<AdvancedMediaPlayer> player;
public:
    explicit MediaAdapter(const std::string& type) {
        if (type == "vlc") player = std::make_unique<VlcPlayer>();
        else if (type == "mp4") player = std::make_unique<Mp4Player>();
    }
    void play(const std::string& type, const std::string& file) override {
        if (!player) return;
        if (type == "vlc") player->playVlc(file);
        else if (type == "mp4") player->playMp4(file);
    }
};

// AudioPlayer with adapter support
class AudioPlayer : public MediaPlayer {
private:
    std::unique_ptr<MediaAdapter> adapter;
public:
    void play(const std::string& type, const std::string& file) override {
        if (type == "mp3") {
            std::cout << "Playing MP3: " << file << "\n";
        } else if (type == "vlc" || type == "mp4") {
            adapter = std::make_unique<MediaAdapter>(type);
            adapter->play(type, file);
        } else {
            std::cout << "Format not supported: " << type << "\n";
        }
    }
};

int main() {
    AudioPlayer player;
    player.play("mp3", "song.mp3");
    player.play("vlc", "video.vlc");
    player.play("mp4", "movie.mp4");
    player.play("avi", "clip.avi");
}"""

BEFORE_CODE = r"""// Without Adapter - client must handle each format
class AudioPlayer {
    void play(string type, string file) {
        if (type == "mp3") { /* play mp3 */ }
        else if (type == "vlc") {
            VlcPlayer vlc;
            vlc.playVlc(file);  // Direct dependency on VLC
        }
        // Tightly coupled to specific players
    }
}"""

AFTER_CODE = r"""// With Adapter - unified interface
class AudioPlayer {
    void play(string type, string file) {
        if (type == "mp3") { /* native */ }
        else {
            adapter = make_unique<MediaAdapter>(type);
            adapter->play(type, file);  // Decoupled
        }
    }
}"""


def demonstrate() -> dict:
    """Execute the Adapter pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Converts the interface of a class into another interface that clients "
            "expect, allowing incompatible classes to work together."
        ),
        "context": (
            "Media player supporting legacy audio/video formats (VLC, MP4) "
            "by adapting them to a common MediaPlayer interface."
        ),
        "pros": [
            "Enables incompatible interfaces to work together",
            "Single Responsibility: adapter separates interface conversion",
            "Open-Closed: add new adapters without changing client code",
        ],
        "cons": [
            "Increases code complexity with additional classes",
            "Indirection can make code harder to follow",
        ],
        "anti_pattern": (
            "Over-Abstraction: Don't create adapters for systems that are already "
            "compatible. Only use adapters when there's a genuine interface mismatch. "
            "Unnecessary adapters add indirection without benefit."
        ),
        "uml_diagram": """
┌─────────────────┐     ┌─────────────────────┐
│  MediaPlayer    │     │ AdvancedMediaPlayer │
├─────────────────┤     ├─────────────────────┤
│ +play(type,file)│     │ +playVlc(file)      │
└────────┬────────┘     │ +playMp4(file)      │
         │              └──────────┬──────────┘
         │                   ┌─────┼──────┐
    ┌────┼────             ▼            ▼
    ▼    ▼    ▼       ┌──────────┐ ┌──────────┐
┌──────┐ │ ┌──────┐  │ VlcPlayer│ │ Mp4Player│
│Audio │─┘ │Media │  └──────────┘ └──────────┘
│Player│   │Adapter│
└──────┘   └───────┘
  (target)   (adapter wraps adaptee)""",
    }
