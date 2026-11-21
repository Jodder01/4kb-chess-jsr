# 4 KB Chess Engine Bounty Research

## Bounty Requirements
- **Language**: Python 3.13 (standard library only)
- **Size Limit**: 4,096 bytes (including newlines)
- **Time Limit**: 10 seconds per move
- **Resources**: 1 CPU, 512 MB RAM, 64 processes
- **Game**: 8 games per trial (openings from book)
- **Opponents**: 8 house engines (2-ply alpha-beta to 2M nodes)
- **Deterministic**: No randomness, fixed search depth/nodes
- **Deadline**: Nov 24, 2026, 5:00 PM UTC
- **Target**: Beat Sunfish 4 KB (1,154 Elo minimum to enter final)

## Sunfish Analysis

### Architecture
- **Board Representation**: 120-character string (10x12 with padding)
- **Move Generation**: Ray-based (sliding pieces by direction)
- **Search**: Negamax with alpha-beta pruning
- **Transposition Tables**: Two tables (tp_score, tp_move)
- **Evaluation**: Piece-square tables (PST) for positional evaluation
- **Enhancements**:
  - Null move pruning (depths 2-6)
  - Futility pruning
  - Killer move heuristic
  - Queen search (depth <= 0)
  - History heuristic
  - Late move reduction (LMR)
  - Mate detection (king capture checks)

### Key Constants
- MATE_LOWER/UPPER: Mate detection bands
- QS: 36 (quiet search threshold)
- QS_A: 180 (quiet search capture value scaling)
- LMR: 70 (late move reduction threshold)
- EVAL_ROUGHNESS: 15
- NULL_MARGIN: -200
- TABLE_SIZE: 1M entries

## Optimization Strategy

### Space Savings Ideas
1. **Compressed PST Tables**: Use arithmetic encoding or run-length encoding
2. **Shorter Identifiers**: Single-letter variables vs full names
3. **Function Folding**: Combine related operations
4. **Magic Numbers**: Pre-compute instead of calculate
5. **Reduced Tables**: Smaller but still effective evaluation tables
6. **Minimal Init**: Only essential board setup
7. **Bitwise Tricks**: Use bit operations for square math

### Strength Improvements
1. **Better Move Ordering**: History table + killer moves
2. **Deeper Search**: More efficient = more nodes
3. **Smarter Pruning**: Fine-tuned thresholds
4. **Tactical Awareness**: Quiescence search tuning
5. **Opening Book**: Key positions hardcoded?
6. **Endgame Tables**: Limited tablebases for common endings

### Testing Strategy
1. Create baseline engine
2. Benchmark against Sunfish with test positions
3. Run tactical/opening/endgame suites
4. Identify weaknesses
5. Iteratively improve and re-benchmark
6. Verify final byte count

## Development Plan
1. Research & analyze Sunfish (CURRENT)
2. Create compact baseline chess engine
3. Implement UCI interface for tournament play
4. Add evaluation and search
5. Optimize for byte count vs strength trade-offs
6. Test against reference engines
7. Final optimization pass
8. Verify requirements and submit
