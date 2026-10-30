const hue = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) % 360, 7)

export function tileBackground(game) {
  if (game.image) return { backgroundImage: `url("${game.image}")` }
  const h = hue(game.title)
  return { backgroundImage: `linear-gradient(135deg, hsl(${h} 70% 45%), hsl(${(h + 60) % 360} 70% 25%))` }
}

export default function Tile({ game, as: Tag = 'div', ...props }) {
  return (
    <Tag className="tile" {...props}>
      <div className="tile-art" style={tileBackground(game)} />
      <div className="tile-info">
        {game.category && <span className="tile-cat">{game.category}</span>}
        <h3>{game.title}</h3>
        {game.description && <p>{game.description}</p>}
      </div>
    </Tag>
  )
}
