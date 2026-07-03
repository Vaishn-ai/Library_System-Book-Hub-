from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from book_app.models import Book, Genre
from .models import ChatMessage
import json
import random


def bookbot_response(user_message, user):
    msg = user_message.lower().strip()

    # Greetings
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good evening', 'sup', 'hlo']
    if any(g in msg for g in greetings):
        return random.choice([
            f"Hi there! 👋 I'm BookBot. Ask me to find books, suggest by genre, or explore the library!",
            f"Hello! 📚 What kind of book are you looking for today?",
            f"Hey! I'm BookBot. I can help you find the perfect book. What genre do you like?",
        ])

    # Thanks
    if any(w in msg for w in ['thank', 'thanks', 'thx', 'ty']):
        return "You're welcome! 😊 Happy reading! 📖"

    # Bye
    if any(w in msg for w in ['bye', 'goodbye', 'see you', 'exit']):
        return "Goodbye! Happy reading! 📚✨"

    # Help
    if 'help' in msg or 'what can you do' in msg:
        return (
            "I can help you with:\n"
            "📚 Find books by genre\n"
            "✍️ Search by author name\n"
            "💰 Find free books\n"
            "📖 Show all available books\n"
            "🏷️ Browse categories\n\n"
            "Just ask me something like:\n"
            "- 'Show me fiction books'\n"
            "- 'Find books by [author name]'\n"
            "- 'What free books are available?'"
        )

    # Show all books
    if any(w in msg for w in ['all books', 'show books', 'list books', 'available books']):
        books = Book.objects.all()
        if not books.exists():
            return "No books in the library yet. Check back soon! 📭"
        lines = [f"📚 We have {books.count()} books:\n"]
        for b in books[:10]:
            price = "FREE" if b.is_free else f"₹{b.price}"
            lines.append(f"• {b.title} by {b.author} [{price}]")
        if books.count() > 10:
            lines.append(f"...and {books.count() - 10} more. Visit /show/ to see all!")
        return "\n".join(lines)

    # Free books
    if any(w in msg for w in ['free', 'no cost', 'without pay', 'free books']):
        books = Book.objects.filter(is_free=True)
        if not books.exists():
            return "No free books available right now. 😔 Check back later!"
        lines = ["🎉 Free books available:\n"]
        for b in books:
            lines.append(f"• {b.title} by {b.author}")
        return "\n".join(lines)

    # Search by author
    if 'by ' in msg or 'author' in msg or 'written by' in msg:
        # extract author name
        for prefix in ['by ', 'author ', 'written by ', 'books by ', 'find by ']:
            if prefix in msg:
                author_name = msg.split(prefix)[-1].strip().title()
                books = Book.objects.filter(author__icontains=author_name)
                if books.exists():
                    lines = [f"📖 Books by '{author_name}':\n"]
                    for b in books:
                        price = "FREE" if b.is_free else f"₹{b.price}"
                        lines.append(f"• {b.title} [{price}]")
                    return "\n".join(lines)
                else:
                    return f"No books found by '{author_name}'. Try a different name!"

    # Search by genre
    genres = Genre.objects.all()
    for genre in genres:
        if genre.name.lower() in msg:
            books = Book.objects.filter(genres=genre)
            if books.exists():
                lines = [f"📚 {genre.name} books:\n"]
                for b in books:
                    price = "FREE" if b.is_free else f"₹{b.price}"
                    lines.append(f"• {b.title} by {b.author} [{price}]")
                return "\n".join(lines)
            else:
                return f"No {genre.name} books yet. More coming soon! 📭"

    # Price / buy
    if any(w in msg for w in ['buy', 'purchase', 'price', 'cost', 'how much']):
        books = Book.objects.filter(is_free=False).order_by('price')
        if not books.exists():
            return "All books are free right now! 🎉"
        lines = ["💰 Paid books (lowest price first):\n"]
        for b in books[:8]:
            lines.append(f"• {b.title} — ₹{b.price}")
        return "\n".join(lines)

    # Categories / genres
    if any(w in msg for w in ['categor', 'genre', 'type', 'kind']):
        genres = Genre.objects.all()
        if not genres.exists():
            return "No categories added yet!"
        names = ', '.join(g.name for g in genres)
        return f"📌 Available categories:\n{names}\n\nAsk me about any of these!"

    # Recommend
    if any(w in msg for w in ['recommend', 'suggest', 'what should i read', 'best book']):
        books = list(Book.objects.all())
        if not books:
            return "No books available yet to recommend! 📭"
        pick = random.choice(books)
        price = "FREE" if pick.is_free else f"₹{pick.price}"
        return (
            f"📖 I recommend:\n\n"
            f"**{pick.title}** by {pick.author}\n"
            f"Price: {price}\n"
            f"Year: {pick.publication_year}\n\n"
            f"Visit the store to buy and read it!"
        )

    # How many books
    if any(w in msg for w in ['how many', 'count', 'total books', 'number of books']):
        count = Book.objects.count()
        free_count = Book.objects.filter(is_free=True).count()
        return (
            f"📊 Library Stats:\n"
            f"• Total books: {count}\n"
            f"• Free books: {free_count}\n"
            f"• Paid books: {count - free_count}"
        )

    # Default fallback
    books = Book.objects.all()
    genre_names = ', '.join(g.name for g in Genre.objects.all())
    return (
        f"Hmm, I'm not sure about that. 🤔\n\n"
        f"I can help you with:\n"
        f"• Browse genres: {genre_names or 'Fiction, Science, History...'}\n"
        f"• Find free books\n"
        f"• Search by author\n"
        f"• Get book recommendations\n\n"
        f"Try: 'Show me fiction books' or 'Recommend something!'"
    )


@login_required(login_url='login_url')
def chat_view(request):
    history = ChatMessage.objects.filter(user=request.user).order_by('created_at')[:50]
    return render(request, 'chat/chat.html', {'history': history})


@login_required(login_url='login_url')
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        ChatMessage.objects.create(
            user=request.user,
            role='user',
            message=user_message
        )

        reply = bookbot_response(user_message, request.user)

        ChatMessage.objects.create(
            user=request.user,
            role='assistant',
            message=reply
        )

        return JsonResponse({'reply': reply})

    except Exception as e:
        print(f"ChatBot Error: {e}")
        return JsonResponse({'reply': 'Sorry, something went wrong. Please try again.'})


@login_required(login_url='login_url')
def clear_chat(request):
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'cleared'})