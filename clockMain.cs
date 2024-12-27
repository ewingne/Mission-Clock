using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace ClockApp
{
    public sealed partial class MainWindow : Window
    {
        private DispatcherTimer timer;

        public MainWindow()
        {
            this.InitializeComponent();
            Title = "Digital Clock";

            // Create the main grid
            Grid mainGrid = new Grid();
            Content = mainGrid;

            // Create the time display TextBlock
            TextBlock timeDisplay = new TextBlock
            {
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center,
                FontSize = 72,
                FontWeight = Microsoft.UI.Text.FontWeights.SemiBold
            };

            mainGrid.Children.Add(timeDisplay);

            // Set up the timer
            timer = new DispatcherTimer();
            timer.Interval = TimeSpan.FromSeconds(1);
            timer.Tick += (s, e) =>
            {
                timeDisplay.Text = DateTime.Now.ToString("HH:mm:ss");
            };
            timer.Start();
        }
    }
}