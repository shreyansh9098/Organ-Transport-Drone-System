import hashlib
import json
from datetime import datetime
from sqlalchemy.orm import Session
import models

class BlockchainLedger:
    """Mock blockchain implementation with hash chaining for immutable telemetry logs"""
    
    @staticmethod
    def create_hash(data: str, previous_hash: str) -> str:
        """Create SHA-256 hash from data and previous hash"""
        block_string = f"{data}{previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    @staticmethod
    def add_telemetry_block(db: Session, mission_id: int, telemetry_data: dict) -> models.BlockchainLedger:
        """Add a new telemetry block to the blockchain"""
        # Get the last block for this mission
        last_block = db.query(models.BlockchainLedger).filter(
            models.BlockchainLedger.mission_id == mission_id
        ).order_by(models.BlockchainLedger.block_index.desc()).first()
        
        if last_block:
            block_index = last_block.block_index + 1
            previous_hash = last_block.current_hash
        else:
            block_index = 0
            previous_hash = "0" * 64
        
        # Prepare data
        data_string = json.dumps(telemetry_data, sort_keys=True)
        current_hash = BlockchainLedger.create_hash(data_string, previous_hash)
        
        # Create new block
        new_block = models.BlockchainLedger(
            mission_id=mission_id,
            block_index=block_index,
            timestamp=datetime.utcnow(),
            data=data_string,
            previous_hash=previous_hash,
            current_hash=current_hash
        )
        
        db.add(new_block)
        db.commit()
        db.refresh(new_block)
        
        return new_block
    
    @staticmethod
    def add_alert_block(db: Session, mission_id: int, alert_data: dict) -> models.BlockchainLedger:
        """Add a new alert block to the blockchain"""
        return BlockchainLedger.add_telemetry_block(db, mission_id, alert_data)
    
    @staticmethod
    def verify_chain(db: Session, mission_id: int) -> bool:
        """Verify the integrity of the blockchain for a mission"""
        blocks = db.query(models.BlockchainLedger).filter(
            models.BlockchainLedger.mission_id == mission_id
        ).order_by(models.BlockchainLedger.block_index).all()
        
        for i, block in enumerate(blocks):
            if i == 0:
                # Genesis block
                if block.previous_hash != "0" * 64:
                    return False
            else:
                # Check if previous hash matches
                if block.previous_hash != blocks[i-1].current_hash:
                    return False
            
            # Verify current hash
            calculated_hash = BlockchainLedger.create_hash(block.data, block.previous_hash)
            if calculated_hash != block.current_hash:
                return False
        
        return True
