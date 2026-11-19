from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

# ساخت جدول‌ها در دیتابیس
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="سیستم حرفه‌ای فروش بلیط")

@app.post("/users", tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ثبت‌نام کاربر جدید"""
    existing_user = db.query(models.UserDB).filter(models.UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="این نام کاربری قبلاً ثبت شده است")
    
    new_user = models.UserDB(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "کاربر با موفقیت ساخته شد", "user": new_user}

@app.get("/tickets", tags=["Tickets"])
def get_tickets(db: Session = Depends(get_db)):
    """مشاهده تمام بلیط‌ها"""
    return db.query(models.TicketDB).all()

@app.post("/tickets", tags=["Tickets"])
def create_ticket(new_ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """ایجاد بلیط جدید"""
    db_ticket = models.TicketDB(event=new_ticket.event, price=new_ticket.price)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return {"message": "بلیط در دیتابیس ذخیره شد", "ticket": db_ticket}

@app.post("/tickets/{ticket_id}/buy", tags=["Tickets"])
def buy_ticket(ticket_id: int, user_id: int, db: Session = Depends(get_db)):
    """خرید بلیط توسط یک کاربر مشخص"""
    user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد! ابتدا ثبت‌نام کنید.")

    ticket = db.query(models.TicketDB).filter(models.TicketDB.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="بلیط پیدا نشد.")
    if not ticket.available:
        raise HTTPException(status_code=400, detail="این بلیط قبلاً فروخته شده است!")
    
    ticket.available = False
    ticket.owner_id = user.id
    db.commit()
    db.refresh(ticket)
    return {"message": f"بلیط با موفقیت توسط {user.username} خریداری شد!", "ticket": ticket}