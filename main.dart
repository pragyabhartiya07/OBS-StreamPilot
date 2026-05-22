import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "OBS Controller",
      theme: ThemeData(
        primarySwatch: Colors.indigo,
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int currentIndex = 0;

  final screens = [
    const DashboardScreen(),
    const SceneScreen(),
    const AudioScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: screens[currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: (index) => setState(() => currentIndex = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: "Dashboard"),
          BottomNavigationBarItem(icon: Icon(Icons.movie), label: "Scenes"),
          BottomNavigationBarItem(icon: Icon(Icons.volume_up), label: "Audio"),
        ],
      ),
    );
  }
}

//////////////////////////////////////////////////
// DASHBOARD
//////////////////////////////////////////////////

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  Widget buildButton(String text, IconData icon, Color color) {
    return ElevatedButton.icon(
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        minimumSize: const Size(double.infinity, 55),
      ),
      onPressed: () {},
      icon: Icon(icon),
      label: Text(text),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Dashboard")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text("Status: 🔴 Offline"),
            const SizedBox(height: 20),

            buildButton("Start Stream", Icons.play_arrow, Colors.green),
            buildButton("Stop Stream", Icons.stop, Colors.red),

            const SizedBox(height: 20),

            buildButton("Start Recording", Icons.fiber_manual_record, Colors.blue),
            buildButton("Stop Recording", Icons.stop_circle, Colors.redAccent),
          ],
        ),
      ),
    );
  }
}

//////////////////////////////////////////////////
// SCENES
//////////////////////////////////////////////////

class SceneScreen extends StatelessWidget {
  const SceneScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final scenes = ["Intro", "Gameplay", "BRB", "Ending"];

    return Scaffold(
      appBar: AppBar(title: const Text("Scenes")),
      body: ListView.builder(
        itemCount: scenes.length,
        itemBuilder: (context, index) {
          return ListTile(
            leading: const Icon(Icons.video_collection),
            title: Text(scenes[index]),
            trailing: ElevatedButton(
              onPressed: () {},
              child: const Text("Switch"),
            ),
          );
        },
      ),
    );
  }
}

//////////////////////////////////////////////////
// AUDIO
//////////////////////////////////////////////////

class AudioScreen extends StatefulWidget {
  const AudioScreen({super.key});

  @override
  State<AudioScreen> createState() => _AudioScreenState();
}

class _AudioScreenState extends State<AudioScreen> {
  double volume = 50;
  bool isMuted = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Audio Control")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text("Microphone"),
            Slider(
              value: volume,
              min: 0,
              max: 100,
              onChanged: (val) {
                setState(() => volume = val);
              },
            ),

            SwitchListTile(
              title: const Text("Mute"),
              value: isMuted,
              onChanged: (val) {
                setState(() => isMuted = val);
              },
            ),
          ],
        ),
      ),
    );
  }
}

