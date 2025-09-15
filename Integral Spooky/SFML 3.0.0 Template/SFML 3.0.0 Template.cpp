// SFML 3.0.0 Template.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <SFML/Graphics.hpp>
#include <IntegralCalculator.cpp>

int main()
{
    sf::RenderWindow window(sf::VideoMode({ 800, 600 }), "SFML works!");
	float centerX = window.getSize().x / 2.f;
	float centerY = window.getSize().y / 2.f;

    // Load Textures

    sf::Texture hqTexture;
    hqTexture.loadFromFile("hq.png");
    hqTexture.setSmooth(false);

    sf::Texture mapTexture;
    mapTexture.loadFromFile("map.png");
    mapTexture.setSmooth(false);

    sf::Texture pinTexture;
    pinTexture.loadFromFile("pins.png");
    pinTexture.setSmooth(false);

    sf::Texture noiseTexture;
    noiseTexture.loadFromFile("perlin noise.jpg");
    noiseTexture.setSmooth(false);

	// Create Sprites & objects
    sf::Sprite hqSprite(hqTexture);
    hqSprite.sf::Transformable::setPosition({ centerX - 32, centerY});

    sf::Sprite map(mapTexture);

    sf::Sprite pin(pinTexture);

    sf::Sprite noise(noiseTexture);

    while (window.isOpen())
    {
        while (const std::optional event = window.pollEvent())
        {
            if (event -> is<sf::Event::Closed>())
                window.close();
        }

        window.clear();
        window.draw(pin);
        window.draw(map);
        window.draw(hqSprite);
        window.display();
    }
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
